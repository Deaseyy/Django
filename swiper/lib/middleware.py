from django.utils.deprecation import MiddlewareMixin

from common import errors
from common.errors import LogicErr
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    '''校验登录状态中间件'''

    def process_request(self, request):
        #白名单
        WHITE_list = [
            '/api/user/submit/phone/',
            '/api/user/submit/vcode/',
        ]

        if request.path in WHITE_list:
            return None

        uid = request.session.get('uid')
        if uid:
            try:
                user = User.objects.get(id=uid)
                request.user = user
                return None
            except User.DoesNotExist:
                return render_json(code=errors.USER_NOT_EXIST, data='用户不存在')
        else:
            return render_json(code=errors.LOGIN_REQUIRED, data='未登录')


class LogicErrMiddleware(MiddlewareMixin):
    '''捕获自定义异常中间件'''

    def process_exception(self, request, exception): # 接收抛出的异常对象
        # 只处理逻辑错误
        if isinstance(exception, LogicErr):
            # print(exception)
            return render_json(code=exception.code, data=exception.data)
