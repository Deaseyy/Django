from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from user.form import RegisterForm, LoginForm


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
