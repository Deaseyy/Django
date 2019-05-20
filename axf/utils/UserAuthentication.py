from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from user.models import AXFUser
from utils import errors


class UserAuth(BaseAuthentication):
    # 用户登陆认证方法, 该方法必须被重构,且返回结构必须为元组(user,token)
    def authenticate(self, request):
        # 判断哪种请求方式能获取到参数
        token = request.query_params.get('token')  # 按get请求获取,
        if not token:                              # 获取不到时
            token = request.data.get('token')      # 按POST请求获取
        # 三元运算写法
        # token = request.query_params.get('token') if request.query_params.get('token') else request.data.get('token')

        # 登陆信息的判断, cache使用
        user_id = cache.get(token)
        if user_id:
            user = AXFUser.objects.filter(pk=user_id).first()
            return user, token
        res = {
            'code': 1007,
            'msg': '请先登陆后再操作'
        }
        raise errors.ParamsException(res)
