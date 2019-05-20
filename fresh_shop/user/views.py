from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


from user.models import User, UserAddress
from user.form import registerForm, loginForm, addressForm
from utils.function import islogin


#登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 表单验证输入是否合法
        form = loginForm(request.POST)
        if form.is_valid():
            # name = request.POST.get('username')
            # clean函数返回值后,用表单forms的方法获取校验后的字段
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first() #表单验证user是已经存在的
            if not check_password(password,user.password):
                return render(request, 'login.html', {'err': '密码错误!'})
            # 设置session,过期时间
            request.session['username'] = user.username
            request.session.set_expiry(86400)
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            return render(request,'login.html', {'form':form})

# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('user_name')
            password = make_password(form.cleaned_data.get('pwd'))
            email = form.cleaned_data.get('email')
            User.objects.create(username=username,password=password,email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request,'register.html', {'form':form})  #通过form.errors获取错误信息


# 退出
def logout(request):
    del request.session['username']
    if request.session.get('session_goods'):
        del request.session['session_goods']
    return HttpResponseRedirect(reverse('user:login'))

# 个人信息
def user_center_info(request):
    name = request.session.get('username')
    user = User.objects.filter(username=name).first()
    return render(request,'user_center_info.html',{'user':user})


# 全部订单
def user_center_order(request):
    return render(request, 'user_center_order.html')


# 收货地址
def user_center_site(request):
    if request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        addr = UserAddress.objects.filter(user_id=user.id).first()
        return render(request, 'user_center_site.html', {'addr':addr})


# 编辑收货地址
def edit_site(request):
    if request.method == 'POST':
        form = addressForm(request.POST)
        if form.is_valid():
            username = request.session.get('username')
            user = User.objects.filter(username=username).first()
            name = form.cleaned_data.get('name')
            site = form.cleaned_data.get('site')
            postcode = form.cleaned_data.get('postcode')
            tel = form.cleaned_data.get('tel')
            #保存数据
            addr = UserAddress()
            addr.signer_name = name
            addr.address = site
            addr.signer_postcode = postcode
            addr.signer_mobile = tel
            addr.user_id = user.id
            addr.save()
            return HttpResponseRedirect(reverse('order:place_order'))
        else:
            error = form.errors
            return render(request, 'user_center_site.html', {'error': error})
