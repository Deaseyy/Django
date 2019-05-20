from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response

from carts.models import Cart
from carts.serializer import CartSerializer
from utils.UserAuthentication import UserAuth


class CartView(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               mixins.UpdateModelMixin):

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = (UserAuth,) # 登陆校验的类,相当于中间件,进入函数就会先调用它,参数后为元组

    #展示购物车商品信息
    def list(self, request,*args, **kwargs):
        # 响应结果为{code:200,msg:'',data:{carts:'',total_price:''}}

        queryset = self.get_queryset()
        # 查找出当前登陆用户的购物车信息
        queryset = queryset.filter(c_user=request.user)
        serializer = self.get_serializer(queryset, many=True)

        # 计算总价
        queryset = queryset.filter(c_is_select=1).all()
        total_price = 0
        for cart in queryset:
            total_price += round(cart.c_goods_num * cart.c_goods.price, 2)

        res = {
            'carts': serializer.data,
            'total_price': total_price,
        }
        return Response(res)


    # 自定义路由添加购物车
    @list_route(methods=['POST'])
    def add_cart(self, request, *args, **kwargs):
        # 思路.登陆和没登录情况,这里会先调用authentication_classes指向的类去校验
        goodsid = request.data.get('goodsid')
        # 2.如果当前登陆系统用户已添加同一商品,则商品数量加一
        #ps: 外键c_user在映射到数据库为user_id,这里都可以使用,
        # request.user取到的是authentication_classes校验返回的参数
        cart = Cart.objects.filter(c_user=request.user, c_goods_id=goodsid).first()
        if not cart:  # 购物车中没有该账号添加的对应商品
            Cart.objects.create(c_user=request.user, c_goods_id=goodsid)
        else:         # 否则,创建购物车中的信息
            cart.c_goods_num += 1
            cart.save()
        res = {
            'code': 200,
            'msg': '添加成功!'
        }
        return Response(res)


    # 修改购物车对象选中状态 c_is_select
    # 前端使用patch请求/api/cart/cart/id/, 重构update方法
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.c_is_select = not instance.c_is_select  # 取反
        instance.save()
        res = {
            'code': 200,
            'msg': '请求成功'
        }
        return Response(res)


    # 自定义路由,修改全选状态
    @list_route(methods=['PATCH'])
    def change_select(self, request, *args, **kwargs):
    # 修改当前登陆用户的购物车中的商品的所有选中状态
        user = request.user
        Cart.objects.filter(c_user=user).update(c_is_select=1)
        res = {
            'code': 200,
            'msg': '请求成功'
        }
        return Response(res)


    # 自定义路由 减少商品数量
    @list_route(methods=['POST'])
    def sub_cart(self, request, *args,**kwargs):
        user = request.user
        goodsid = request.data.get('goodsid')
        carts = Cart.objects.filter(c_user=user, c_goods_id=goodsid).first()

        res = {'code': 200, 'msg': '操作成功'}
        if not carts:   # 防止后台数据丢失后出错
            # 购物车中没有该商品信息
            res = {
                    'code': 1008,
                    'msg': '购物车没有该商品,无法操作!'
                   }
        if carts.c_goods_num > 1:
            # 更新,减少商品的数量,减一操作
            carts.c_goods_num -= 1
            carts.save()
        else:
            # 当商品的数量为一的时候,删除商品信息
            carts.delete()
        return Response(res)
