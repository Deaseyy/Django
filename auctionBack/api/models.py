from django.db import models

class User(models.Model):
    phone = models.CharField(verbose_name='手机号',max_length=11,unique=True)
    nick = models.CharField(verbose_name='昵称',max_length=255, null=True,blank=True)
    avatar = models.CharField(verbose_name='头像地址',max_length=500, null=True,blank=True)
    # token = models.CharField(verbose_name='手机号',max_length=64,null=True,blank=True)

    class Meta:
        db_table= 'user'


class Photos(models.Model):
    img_url = models.CharField(verbose_name='图片地址', max_length=1000)
    add_time = models.DateTimeField(verbose_name='添加时间', null=True,blank=True,auto_now_add=True)

    class Meta:
        db_table= 'photos'


# class LifeDynamic(models.Model):
#     user_id = models.IntegerField(verbose_name="用户(id)", default=None)
#     images = models.CharField(verbose_name="图片地址", max_length=1500, null=True,blank=True)
#     content = models.CharField(verbose_name="内容", max_length=500, null=True,blank=True)
#     site = models.CharField(verbose_name="地点", max_length=100, null=True,blank=True)
#     tag = models.CharField(verbose_name="标签", max_length=300, null=True,blank=True)
#     add_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True)
#     like = models.IntegerField(verbose_name="点赞数", default=0)
#
#     class Meta:
#         db_table= 'lifedynamic'
#
#     @property
#     def user(self):
#         return UserInfo.objects.get(id=self.user_id)