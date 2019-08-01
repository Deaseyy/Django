from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.form import RegisterForm, LoginForm, MyLoginForm
from user.models import MyUser, MyUserToken
from utils.functions import get_token, is_login, is_session_login


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 获取数据
        # username = request.POST.get('username')
        # password1 = request.POST.get('pwd1')
        # password2 = request.POST.get('pwd2')
        # if not (username and password2 and password1):
        #     pass
        # if not(len(username) > 10 and len(username < 20)):
        #     pass
        # if password1 != password2:
        #     pass
        # 使用表单做验证，验证传递的参数是否满足条件
        form = RegisterForm(request.POST)
        # is_valid(): 判断表单校验参数是否通过，如果通过则返回true，否则返回false
        if form.is_valid():
            # 表示表单校验通过
            # 1. 账号一定不存在
            # 2. 密码和确认密码相等
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pwd1')
            # make_password()
            User.objects.create_user(username=username,
                                     password=password)
            # return HttpResponse('注册账号成功')
            return HttpResponseRedirect(reverse('user:login'))
        # 表示表单校验失败
        errors = form.errors
        return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 使用表单校验post传递的参数
        form = LoginForm(request.POST)
        if form.is_valid():
            # 如果成功
            user = auth.authenticate(username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password'))
            auth.login(request, user)
            return render(request, 'index.html')
        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return render(request, 'index.html')


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def my_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 表单校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 表单校验成功
            username = form.cleaned_data.get('username')
            password = make_password(form.cleaned_data.get('pwd1'))
            MyUser.objects.create(username=username,
                                  password=password)
            # 重定向到登录页面
            return HttpResponseRedirect(reverse('user:my_login'))
        errors = form.errors
        return render(request, 'register.html', {'errors': errors})


def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = MyLoginForm(request.POST)
        if form.is_valid():
            # 1. 只校验的字段username和password的长度，必填等信息
            # 2. 用户名必须存在my_user表中
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = MyUser.objects.get(username=username)
            # 校验密码是否一致
            if not check_password(password, user.password):
                pwd_error = '密码错误'
                return render(request, 'login.html', {'pwd_error': pwd_error})
            # 用户名和密码验证成功了，需要使用cookie+token进行登录身份标识
            res = HttpResponseRedirect(reverse('user:my_index'))
            token = get_token()
            res.set_cookie('token', token, max_age=86400)
            # res.delete_cookie('token')
            # 后端保存token参数值，用于用户下次访问时进行判断
            out_time = datetime.utcnow() + timedelta(days=1)
            my_token = MyUserToken.objects.filter(user_id=user.id).first()
            if my_token:
                my_token.token = token
                my_token.out_time = out_time
                my_token.save()
            else:
                MyUserToken.objects.create(token=token,
                                           user=user,
                                           out_time=out_time)
            return res

        errors = form.errors
        return render(request, 'login.html', {'errors': errors})

# @is_session_login
def my_index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def my_session_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = MyLoginForm(request.POST)
        if form.is_valid():
            # 1. 只校验的字段username和password的长度，必填等信息
            # 2. 用户名必须存在my_user表中
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = MyUser.objects.get(username=username)
            # 校验密码是否一致
            if not check_password(password, user.password):
                pwd_error = '密码错误'
                return render(request, 'login.html', {'pwd_error': pwd_error})
            # 用户名和密码验证成功了，需要使用session
            res = HttpResponseRedirect(reverse('user:my_index'))
            # 向session中存储user_id
            # 1. 向cookie中存储键值对，key为sessionid，value为唯一的值
            # 2. 向django_session表中存sessionid值
            request.session['user_id'] = user.id
            # 设置过期时间
            request.session.set_expiry(86400)
            return res

        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


# @is_session_login
def my_session_logout(request):
    if request.method == 'GET':
        # auth.logout ===> 1. request.user  2. session中数据清空
        # del request.session['user_id']

        # 将cookie中的sessionid值删掉，并且django_session表中的数据删掉
        # request.session.flush()

        # 将django_session表中的数据删掉
        session_key = request.session.session_key
        request.session.delete(session_key)
        return HttpResponse('注销成功')
