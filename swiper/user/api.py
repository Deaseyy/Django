# from django.http import JsonResponse
# from django.shortcuts import render

# Create your views here.
from urllib.parse import urljoin

from django.core.cache import cache

from lib.http import render_json  # 自己封装的返回json的函数, 相当于JsonResponse
from common import errors, keys
from lib.qiniuyun import upload_qiniu
from lib.sms import send_vcode
from swiper import config
from user.forms import ProfileForm
from user.logic import handle_uploaded_file
from user.models import User


def submit_phone(request):
    '''提交手机号用于获取验证码'''

    phone = request.POST.get('phone')
    # 给该手机号发送验证码
    # msg = send_vcode(phone)
    # if msg == 'OK':
    #     return render_json({'code': 0, 'data': None})
    # return render_json({'code':errors.SMS_ERROR, 'data':msg})

    send_vcode.delay(phone)  # 异步任务
    return render_json()


def submit_vcode(request):
    """通过验证码登陆, 注册"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取验证码
    cached_vcode = cache.get(keys.VCODE_KEY % phone)

    if vcode == cached_vcode:
        # 登陆或者注册成功
        # 如果是注册, 在数据库中创建用户
        # 如果是登陆, 直接从数据库查询用户, 返回用户信息
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册, 去数据库中创建用户
        #     user = User.objects.create(phonenum=phone, nick=phone)

        user, created = User.objects.get_or_create(phonenum=phone,)
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    return render_json(code=errors.VCODE_ERROR, data='验证码错误')



def get_profile(request):
    """获取个人资料"""
    # uid = request.session.get('uid')  # 在中间件中将uid对应user绑在request上
    user = request.user
    # 先从缓存中拿
    key = keys.PROFILE_KEY % user.id
    data = cache.get(key)
    if not data:
        # 从数据库拿
        data = user.profile.to_dict()
        print('get from database')
        # 同时存入缓存中
        cache.set(key, data, 14*86400)
    return render_json(data=data)


def edit_profile(request):
    """修改个人资料"""
    user = request.user
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False) # 继承了ModelForm, form相当于Model对象, commit=False 先不提交, 返回一个profile对象
        profile.id = user.id
        profile.save()  # 这里save()相当于更新该id对应数据

        # 更新到缓存
        key = keys.PROFILE_KEY % user.id
        cache.set(key, profile.to_dict(), 86400*14)
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERR, data=form.errors)


def upload_avatar(request):
    """头像上传"""
    avatar = request.FILES.get('avater')
    user = request.user
    uid = user.id

    #保存到本地,并上传到七牛云
    handle_uploaded_file.delay(uid, avatar)

    # 拼接url,存入数据库
    avatar_url = urljoin(config.QINIU_URL, keys.AVATAR_KEY % uid)
    user.avatar = avatar_url
    user.save()
    return render_json(data='上传头像成功')

