
import uuid
from functools import wraps
from datetime import datetime

from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import MyUserToken


def get_token():
    # 获取随机且唯一的token参数
    token = uuid.uuid4().hex
    return token


def is_login(func):
    @wraps(func)
    def check(request, *args, **kwargs):
        # token的校验
        # 1. 查询my_token表中的数据
        # 2. 对比失效时间
        token = request.COOKIES.get('token')
        my_token = MyUserToken.objects.filter(token=token).first()
        if not my_token:
            # 通过前端传递的token值去数据库中查询数据，找不到的情况
            return HttpResponseRedirect(reverse('user:my_login'))
        if my_token.out_time.replace(tzinfo=None) < datetime.utcnow():
            # 将带有时区的时间进行转换
            return HttpResponseRedirect(reverse('user:my_login'))
        return func(request, *args, **kwargs)
    return check


def is_session_login(func):
    def check(request, *args, **kwargs):
        try:
            # 从session中取数据，如果取得出user_id，表示登录
            request.session['user_id']
            return func(request, *args, **kwargs)
        except:
            return HttpResponseRedirect(reverse('user:my_session_login'))
    return check




