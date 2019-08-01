def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """
    return {
        'token': token,
        'id': user.id,
        'username': user.username
    }

from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
import re

def get_user_by_account(account):
    """根据账号信息获取用户模型"""
    try:
        # if re.match('^1[3-9]\d{9}$', account):
        #     # 手机号
        #     user = User.objects.get(mobile=account)
        # else:
        #     # 用户名
        #     user = User.objects.get(username=account)

        user = User.objects.get(Q(mobile=account) | Q(username=account))

    except User.DoesNotExist:

        user = None

    return user


class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 进行登录判断

        user = get_user_by_account(username)

        # 账号通过了还要进行密码的验证,以及判断当前站好是否是激活状态
        if isinstance(user,User) and user.check_password(password) and self.user_can_authenticate(user):
            return user
