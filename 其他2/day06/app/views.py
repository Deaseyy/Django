from django.contrib.auth.models import Permission, Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import NewUser


def index(request):
    # return HttpResponse('index')
    # 实现重定向
    # 第一种方式，无参情况，硬编码重定向地址
    # return HttpResponseRedirect('/app/redirect_no_params/')
    # 第二种方式，无参情况，反向解析出重定向地址
    # 格式： reverse('namespace:name')
    # print(reverse('app:no_params'))
    # return HttpResponseRedirect(reverse('app:no_params'))

    # flask中url_for('蓝图第一个参数.函数名', 参数名=值, xxx=xx)
    # 第一种方式，有参情况，硬编码重定向地址
    # return HttpResponseRedirect('/app/redirect_params/12/')
    # 第二种方式，有参情况，反向解析并传递参数
    # return HttpResponseRedirect(reverse('app:params', kwargs={'id': 13}))
    # return HttpResponseRedirect(reverse('app:params', args=(20,)))
    # return HttpResponseRedirect(reverse('app:params2', args=(18,)))

    return render(request, 'index.html')


def redirect1(request):
    # 从/app/index/路由跳转到该方法
    return render(request, 'index.html')


def redirect2(request, id):
    # 从/app/index/路由跳转到该方法，并接收传递的参数
    return render(request, 'index.html', {'id': id})


def index2(request):
    # 判断请求方式 method
    # 获取参数，GET请求时，request.GET.get()  getlist()
    # POST请求时，request.POST.get()  getlist()
    # 获取文件，FILES
    # 请求地址, path
    # 请求中的cookie值，COOKIES
    # 请求中session数据，session
    # 请求中user对象，默认匿名用户
    if request.method == 'GET':
        # 响应数据
        # HttpResponse(数据)
        # render(页面)
        # HttpResponseRedirect(地址)
        # JsonResponse(json数据)
        # return HttpResponse('index2')
        return JsonResponse({'code': 200, 'msg': '请求成功'})

    if request.method == 'POST':

        return HttpResponse('index2 post')


def add_permission(request):
    if request.method == 'GET':
        # 用户分配角色和权限
        permissions = Permission.objects.filter(codename__in=['add',
                                                'sel', 'update',
                                                'delete']).all()
        goups = Group.objects.all()
        user = NewUser.objects.get(username='coco')
        request.user = user
        return render(request, 'perms.html', {'permissions': permissions,
                                              'goups': goups})

    if request.method == 'POST':
        # 使用login_required装饰
        # user = request.user
        # 没有使用login_required装饰
        user = NewUser.objects.get(username='coco')
        role_id = request.POST.get('role')
        per_id = request.POST.getlist('per')
        # 用户分配角色
        role = Group.objects.get(pk=role_id)
        user.groups.add(role)
        # 角色分配权限
        for id in per_id:
            p = Permission.objects.get(pk=int(id))
            role.permissions.add(p)

        return HttpResponse('分配成功')


def menu(request):
    if request.method == 'GET':
        return render(request, 'menu.html')


