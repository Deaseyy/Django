from django.db import models


class MyUser(models.Model):
    username = models.CharField(max_length=10,null=False, unique=True,
                                verbose_name='账号')
    password = models.CharField(max_length=255, null=False,
                                verbose_name='密码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    # 头像: 1. 存图片本身还是图片的地址？   2. 图片地址绝对路径还是相对路径
    icon = models.ImageField(upload_to='upload', null=True)

    class Meta:
        db_table = 'my_user'


class MyUserToken(models.Model):
    token = models.CharField(max_length=100, unique=True, null=False,
                             verbose_name='token标识符')
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    out_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'my_token'

