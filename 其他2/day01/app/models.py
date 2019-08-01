from django.db import models


class Article(models.Model):
    # 唯一、不能为空且长度不能超过10字符的title字段
    title = models.CharField(max_length=10, unique=True, null=False)
    desc = models.TextField(null=False)
    is_delete = models.BooleanField(default=0)

    class Meta:
        db_table = 'article'


class Student(models.Model):
    # 最大长度为10字符，不能为空，唯一
    s_name = models.CharField(max_length=10, unique=True,
                              null=False, verbose_name='id')
    s_age = models.IntegerField(default=20, verbose_name='年龄')
    # auto_now_add: 创建数据时，默认赋予创建时间
    create_time = models.DateTimeField(auto_now_add=True,
                                       verbose_name='创建时间')
    # auto_now: 修改数据时，默认赋予修改的时间
    operate_time = models.DateTimeField(auto_now=True,
                                        verbose_name='修改时间')
    # TimeField
    # DateField
    # ImageField
    # DecimalField
    # FloatField
    # BooleanField
    # AutoField

    class Meta:
        db_table = 'student'

