from django.shortcuts import render

# Create your views here.
from django.core.cache import cache
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from carts.models import Cart
from orders.filters import OrderFilter
from orders.models import Order, OrderGoods
from orders.serializers import OrderSerializer, OrderGoodsSerializer
from utils.UserAuthentication import UserAuth


class OrdersView(viewsets.GenericViewSet,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_class = OrderFilter
    # 用户认证
    authentication_classes = (UserAuth,) #必须是元组

    # 商品订单页面展示
    # # list方法返回结构:{code:200,msg:'',data[{订单,order_goods_info}]}
    # 方法一: 重构list中get_queryset方法, 序列化类中再重构to_representation,
    def get_queryset(self):   # 默认返回queryset
        return self.queryset.filter(o_user=self.request.user)

    # 方法二: 重构list方法
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(o_user=request.user)
    #     serializer = self.get_serializer(queryset, many=True)
    #     for order in serializer.data:
    #         order_goods = OrderGoods.objects.filter(o_order_id=order['id']).all()
    #         order['order_goods_info'] = OrderGoodsSerializer(order_goods,many=True).data
    #     return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        # 创建订单和订单详情表内容
        # token = request.query_params.get('token')
        # user_id = cache.get(token)
        # carts = Cart.objects.filter(c_user_id=user_id,c_is_select=1).all()
        # 用户校验中已经返回user,token, 直接用request.user获取登陆用户
        carts = Cart.objects.filter(c_user=request.user,c_is_select=1).all()
        if carts:
            total_price = 0
            for cart in carts:
                total_price += cart.c_goods_num * cart.c_goods.price
            # 创建订单
            order = Order.objects.create(o_price=total_price, o_user=request.user)
            # 创建订单中商品详情
            for cart in carts:
                OrderGoods.objects.create(o_order=order,
                                        o_goods=cart.c_goods,
                                        o_goods_num=cart.c_goods_num)
                cart.delete() # 删除购物车中商品信息

            res={
                'code': 200,
                'msg': '下单OK!'
            }
            return Response(res)

        res = {
            'code': 1009,
            'msg': '购物车中没有商品,请先添加!'
        }
        return Response(res)



