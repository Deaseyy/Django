from django.contrib.auth.models import User, AbstractUser
from django.db import models


# 扩展django自带的User模型，并自定义其他的权限
class NewUser(AbstractUser):

    is_delete = models.BooleanField(default=0)

    class Meta:
        permissions = (
            ('add', '新增用户'),
            ('delete', '删除用户'),
            ('update', '更新用户'),
            ('sel', '查看用户')
        )