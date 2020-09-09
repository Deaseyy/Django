# todo 暂时没有启用下面的认证组件
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler

from api.models import User
from utils import errors


class UserAuth(BaseAuthentication):
    # 用户登陆认证方法, 该方法必须被重构,且返回结构必须为元组(user,token)
    def authenticate(self, request):
        # # 判断哪种请求方式能获取到参数
        # token = request.query_params.get('token')  # 按get请求获取,
        # if not token:                              # 获取不到时
        #     token = request.data.get('token')      # 按POST请求获取
        token = request.META.get('HTTP_AUTHORIZATION', None)

        # 登陆判断 验证jwt
        try:
            payload = jwt_encode_handler(token)
        except:
            res = {
                'code': 1007,
                'msg': '未登录！'
            }
            raise errors.ParamsException(res)
        user =  User.objects.get(phone=payload['phone'])
        return user, token     # 返回的user会设置到request.user上(request.user默认是匿名用户)




class GeneralAuthentication(BaseAuthentication):
    """
    通用认证：如果认证成功则返回数据，认证失败自己不处理，交给下一个认证组件处理
    如果只使用这一个认证类：那么登录和不登陆都可以进入view，只是登陆后有用户信息，没登陆没有；
    在程序中判断request.user是否有值即可
    """
    def authentication(selfself,request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None  # 返回None 表示自己不处理，交给下一个认证组件

        user_obj = User.objects.filter(token=token).first()
        if not user_obj:
            return None

        return user_obj,token   # request.user/request.auth


class UserAuthentication:
    """用户认证，用户必须先登录"""

    def authentication(selfself, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            raise exceptions.AuthenticationFailed()   # 会返回一个403状态码

        user_obj = User.objects.filter(token=token).first()
        if not user_obj:
            raise exceptions.AuthenticationFailed()

        return user_obj, token  # request.user/request.auth