from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import MyUser


class Test1Middleware(MiddlewareMixin):

    def process_request(self, request):
        # 请求之前被调用
        print('test1 middleware request')
        # return HttpResponse('hello')
        return None
        # return None以下的代码不再执行
        print('test1')

    def process_response(self, request, response):
        # 请求之后被调用
        print('test1 middleware reponse')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        print('test1 middleware view')


class Test2Middleware(MiddlewareMixin):

    def process_request(self, request):
        # 请求之前被调用
        print('test2 middleware request')

    def process_response(self, request, response):
        # 请求之后被调用
        print('test2 middleware reponse')
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('test2 middleware view')


class UserLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 登录校验中间件
        # 过滤不需要做登录校验的地址
        path = request.path
        if path in ['/user/my_register/', '/user/my_login/',
                    '/user/my_session_login/']:
            return None

        # 做登录校验
        user_id = request.session.get('user_id')
        if not user_id:
            return HttpResponseRedirect(reverse('user:my_session_login'))
        user = MyUser.objects.get(pk=user_id)
        request.user = user

