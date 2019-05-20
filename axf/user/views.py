from django.shortcuts import render
from rest_framework import viewsets,mixins

from django.core.cache import cache
# Create your views here.
from rest_framework.decorators import list_route
from rest_framework.response import Response

from orders.models import Order
from user.models import AXFUser
from user.serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from utils.errors import ParamsException


class UserView(viewsets.GenericViewSet, # 提供两个方法 get_object get_queryset,也可以直接继承generics.GenericAPIView
               mixins.ListModelMixin,
               mixins.CreateModelMixin):

    queryset = AXFUser.objects.all()
    serializer_class = UserSerializer

    # 参数获取
    # get请求传的参,或问号后传参使用request.query_params.get()获取
    # post请求传的参, 使用request.data.get()获取

    # 用于返回登录用户信息
    def list(self, request,*args,**kwargs):
        # 1. 先获取前端请求中传递的token
        token = request.query_params.get('token')
        # 2. 通过token从redis中取用户的id值
        user_id = cache.get(token)
        # 3. 序列化用户对象
        user = AXFUser.objects.filter(id=user_id).first()
        serializer = self.get_serializer(user)
        # TODO: 订单的待付款和待收货后面再做
        orders_not_pay_num = len(Order.objects.filter(o_user=user, o_status=0).all())
        orders_not_send_num = len(Order.objects.filter(o_user=user, o_status=2).all())

        res = {
            # 当前登陆系统用户的信息
            'user_info': serializer.data,
            # 订单未支付数量
            'orders_not_pay_num': orders_not_pay_num,
            # 订单未发货数据信息
            'orders_not_send_num': orders_not_send_num,
        }
        return Response(res)


    # 使用list_router装饰,函数名会成为路由中的一部分
    @list_route(methods=['POST'], serializer_class=UserRegisterSerializer)
    def register(self,request,*args, **kwargs):
        # /api/user/auth/register/
        serializer = self.get_serializer(data=request.data) # get_serializer()首先调用的是自己定义的serializer_class=UserRegisterSerializers
        result = serializer.is_valid(raise_exception=False)  #False 不直接抛错
        if not result:
            raise ParamsException({
                'code': 1000,
                'msg': '参数校验失败',
                'data': serializer.errors  # serializer.errors 获取字段校验(上面定义部分)不通过时抛出的错误
            })
        # 保存用户信息
        user = serializer.register_user(serializer.data)
        # 返回结构{'code':200,'msg':'请求成功,'data':{'user_id':user.id}}
        res = {
            'user_id': user.id
        }
        return Response(res)


    @list_route(methods=['POST'],serializer_class=UserLoginSerializer)
    def login(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        result = serializer.is_valid(raise_exception=False)
        if not result:
            raise ParamsException({'code': 1006,'msg':'登陆参数有误!'})
        # 登陆用户
        token = serializer.login_user(serializer.data)
        # 登陆返回结构: {'code':200,'msg':'','data':{token:token值}}
        res = {
            'token': token
        }
        return Response(res)