'''封装将对象转化为python字典的类, 用于继承'''
from django.core.cache import cache
from django.db import models

from common import keys


class ModelMixin:
    def to_dict(self):
        att_dict = {}
        print(self._meta.get_fields())  # _meta可以获取模型的所有字段

        for field in self._meta.get_fields():
            att_dict[field.attname] = getattr(self, field.attname, None)
        return att_dict

    # 对objects.get返回的对象做缓存
    # def get(cls, *args, **kwargs):
    #     obj = cache.get(key)
    #     if not obj:
    #         obj = cls.get(*args, **kwargs)
    # 该方法不能对数据修改后，缓存的更新，使用以下方法：
'''所有模型都继承自models.Model, 可以给这个类添加一些方法，去实现加缓存的操作'''

# 自定义方法，将查询的objects.get()封装进get()，加入缓存和缓存更新功能
def get(cls, *args, **kwargs):
    # 先从缓存中取数据
    # 只针对主键和id的查询进行缓存（只对经常用到的查询做缓存）
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk:
        # 如果是主键才去做缓存
        key = keys.OBJ_KEY % pk
        obj = cache.get(key)
        if not obj:
            # 从数据中拿
            obj = cls.object.get(pk=pk)
            print('get object from database')
            # 存入缓存
            cache.set(key, obj, 86400*15)
    else:
        obj = cls.object.get(*args, **kwargs)  # 正常从数据库取数据
    return obj


#自定义方法，将 get_or_create() 进行封装
def get_or_create(cls, *args, **kwargs):
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk:
        # 如果是主键的话才去做缓存
        key = keys.OBJ_KEY % pk
        obj = cache.get(key)
        if not obj:
            # 从数据库中拿
            obj = cls.objects.get_or_create(pk=pk)
            print('get object from database')
            # 存入缓存
            cache.set(key, obj, 86400 * 15)
    else:
        obj = cls.objects.get_or_create(*args, **kwargs)
    return obj


# create会默认调用Model类中save()方法
# 自定义save方法，这将覆盖Model中的方法，使用ori_save引用原save(),并动态添加到Model类上
def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
    # 需先执行原来自带的save()方法,保存到数据库
    self.ori_save()   # 引用了save()，动态加到Model类上
    # 更新缓到存
    key = keys.OBJ_KEY % self.id
    cache.set(key, self, 86400 * 15)


# 将以上自定义的方法动态添加到Model类，需在User这些模型继承Model之前就添加上，才起作用
# 在 swiper的__init__.py中执行该方法，项目启动时就会先执行
def model_patch():
    # 给django的Model类动态添加get, get_or_create方法
    models.Model.get = classmethod(get)  # 相当于@classmethod装饰get（）
    models.Model.get_or_create = classmethod(get_or_create)
    # 把原生的save取个别名
    # 再将自定义的save存入，当调用save时，就会调用封装了原生save的自定义save
    models.Model.ori_save = models.Model.save
    models.Model.save = save

