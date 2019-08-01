import uuid

from alipay import AliPay
from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from AXFREST.settings import ALIPAY_APPID, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY
from App.authentications import UserTokenAuthentications
from App.models import MainShow, MainWheel, MainNav, MainMustBuy, MainShop, FoodType, Goods, AXFUser, Order, \
    ORDER_STATUS_NOT_SEND, Cart, OrderGoods, ORDER_STATUS_NOT_PAY
from App.permissions import UserLoginPermission
from App.serializers import MainShowSerializer, MainWheelSerializer, MainNavSerializer, MainMustBuySerializer, \
    MainShopSerializer, FoodTypeSerializer, GoodsSerializer, AXFUserSerializer, CartSerializer, OrderSerializer


class MainAPIView(APIView):

    def get(self, request, *args, **kwargs):
        main_wheels = MainWheel.objects.all()
        main_navs = MainNav.objects.all()
        main_mustbuys = MainMustBuy.objects.all()
        main_shops = MainShop.objects.all()
        main_shows = MainShow.objects.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": {
                "main_wheels": MainWheelSerializer(main_wheels, many=True).data,
                "main_navs": MainNavSerializer(main_navs, many=True).data,
                "main_mustbuys": MainMustBuySerializer(main_mustbuys, many=True).data,
                "main_shops": MainShopSerializer(main_shops, many=True).data,
                "main_shows": MainShowSerializer(main_shows, many=True).data
            }
        }

        return Response(data)


class FoodTypeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        food_types = FoodType.objects.all()

        data = {
            "msg": "ok",
            "status": 200,
            "data": FoodTypeSerializer(food_types, many=True).data
        }

        return Response(data)


TYPE_HOT = "104749"

ALL_TYPE = "0"

ORDER_RULE_DEFAULT = "0"
ORDER_RULE_PRICE_UP = "1"
ORDER_RULE_PRICE_DOWN = "2"
ORDER_RULE_SALE_UP = "3"
ORDER_RULE_SALE_DOWN = "4"


class MarketAPIView(APIView):

    def get(self, request, *args, **kwargs):

        typeid = request.query_params.get("typeid") or TYPE_HOT
        childcid = request.query_params.get("childcid") or ALL_TYPE
        order_rule = request.query_params.get("order_rule") or ORDER_RULE_DEFAULT

        if typeid == "":
            typeid = TYPE_HOT

        goods_list = Goods.objects.filter(categoryid=typeid)

        if childcid == ALL_TYPE:
            pass
        else:
            goods_list = goods_list.filter(childcid=childcid)

        if order_rule == ORDER_RULE_DEFAULT:
            pass
        elif order_rule == ORDER_RULE_PRICE_UP:
            goods_list = goods_list.order_by("price")
        elif order_rule == ORDER_RULE_PRICE_DOWN:
            goods_list = goods_list.order_by("-price")
        elif order_rule == ORDER_RULE_SALE_UP:
            goods_list = goods_list.order_by("productnum")
        elif order_rule == ORDER_RULE_SALE_DOWN:
            goods_list = goods_list.order_by("-productnum")

        foodtype = FoodType.objects.get(typeid=typeid)

        foodtypechildnames = foodtype.childtypenames

        foodtypechildname_list = foodtypechildnames.split("#")

        foodtype_childname_list = []

        for foodtypechildname in foodtypechildname_list:
            foodtype_childname = dict()
            foodtype_childname_split = foodtypechildname.split(":")
            foodtype_childname['child_name'] = foodtype_childname_split[0]
            foodtype_childname['child_value'] = foodtype_childname_split[1]
            foodtype_childname_list.append(foodtype_childname)

        order_rule_list = [
            {
                "order_name": "综合排序",
                "order_value": ORDER_RULE_DEFAULT
            },
            {
                "order_name": "价格升序",
                "order_value": ORDER_RULE_PRICE_UP
            },
            {
                "order_name": "价格降序",
                "order_value": ORDER_RULE_PRICE_DOWN
            },
            {
                "order_name": "销量升序",
                "order_value": ORDER_RULE_SALE_UP
            },
            {
                "order_name": "销量降序",
                "order_value": ORDER_RULE_SALE_DOWN
            },
        ]

        data = {
            "msg": "ok",
            "status": 200,
            "data": {
                "order_rule_list": order_rule_list,
                "goods_list": GoodsSerializer(goods_list, many=True).data,
                'foodtype_childname_list': foodtype_childname_list,
            }

        }

        return Response(data)


class AXFUserAPIView(CreateAPIView):
    serializer_class = AXFUserSerializer
    queryset = AXFUser.objects.all()
    authentication_classes = (UserTokenAuthentications,)
    permission_classes = (UserLoginPermission,)

    def get(self, request, *args, **kwargs):

        user = request.user

        orders_not_pay = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY)
        orders_not_send = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_SEND)

        data = {
            "status": 200,
            "msg": "ok",
            "data": {
                "user_info": self.get_serializer(user).data,
                "orders_not_pay_num": orders_not_pay.count() or 0,
                "orders_not_send_num": orders_not_send.count() or 0,
            }
        }

        return Response(data)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")

        if action == "register":

            response = self.create(request, *args, **kwargs)

            data = {
                "msg": "注册成功",
                "status": 200,
                "data": response.data
            }

            return Response(data)
        elif action == "login":
            u_username = request.data.get("u_username")
            u_password = request.data.get("u_password")

            users = AXFUser.objects.filter(u_username=u_username)

            data = {}

            if users.exists():
                user = users.first()

                if user.verify_password(u_password):
                    # if user.is_active:

                    token = uuid.uuid4().hex

                    cache.set(token, user.id, timeout=60 * 60 * 7 * 24)

                    data["msg"] = "登录成功"
                    data["status"] = 200
                    data["data"] = {
                        "token": token
                    }
                # else:
                #     data["msg"] = "用户未激活"
                #     data["status"] = 403
                else:
                    data["msg"] = "密码错误"
                    data["status"] = 401
            else:
                data["msg"] = "用户不存在"
                data["status"] = 404
            return Response(data)

        elif action == "checkname":
            u_username = request.data.get("u_username")
            data = dict()
            if not AXFUser.objects.filter(u_username=u_username).exists():
                data["msg"] = "用户名可用"
                data["status"] = 200
            else:
                data["msg"] = "用户名已存在"
                data["status"] = 400

            return Response(data)

        else:

            data = {
                "msg": "error",
                "status": 400,
                "data": "请提供正确的动作"
            }

            return Response(data)


class CartAPIView(APIView):
    authentication_classes = (UserTokenAuthentications,)
    permission_classes = (UserLoginPermission,)

    def get(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        data = {}

        if action == "add_to_cart":
            goodsid = request.query_params.get("goodsid")
            carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)

            if carts.exists():
                cart_obj = carts.first()
                cart_obj.c_goods_num = cart_obj.c_goods_num + 1
            else:
                cart_obj = Cart()
                cart_obj.c_goods_id = goodsid
                cart_obj.c_user = request.user

            cart_obj.save()

            data = {
                'status': 200,
                'msg': 'add success',
                'c_goods_num': cart_obj.c_goods_num
            }

        elif action == "change_cart_status":
            cart_id = request.GET.get('cartid')

            cart_obj = Cart.objects.get(pk=cart_id)

            cart_obj.c_is_select = not cart_obj.c_is_select

            cart_obj.save()

            is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

            data = {
                'status': 200,
                'msg': 'change ok',
                'c_is_select': cart_obj.c_is_select,
                'is_all_select': is_all_select,
                'total_price': get_total_price(self.request)
            }
            return Response(data)
        elif action == "add_shopping":
            cartid = request.GET.get("cartid")

            cart_obj = Cart.objects.get(pk=cartid)

            data = {
                'status': 200,
                'msg': 'ok',
            }

            cart_obj.c_goods_num = cart_obj.c_goods_num + 1
            cart_obj.save()
            data['c_goods_num'] = cart_obj.c_goods_num
            data['total_price'] = get_total_price(self.request)
            return Response(data)
        elif action == "sub_shopping":
            cartid = request.GET.get("cartid")

            cart_obj = Cart.objects.get(pk=cartid)

            data = {
                'status': 200,
                'msg': 'ok',
            }

            if cart_obj.c_goods_num > 1:
                cart_obj.c_goods_num = cart_obj.c_goods_num - 1
                cart_obj.save()
                data['c_goods_num'] = cart_obj.c_goods_num
            else:
                cart_obj.delete()
                data['c_goods_num'] = 0

            data['total_price'] = get_total_price(self.request)
            return Response(data)
        elif action == "all_select":
            cart_list = request.GET.get('cart_list')

            cart_list = cart_list.split("#")

            carts = Cart.objects.filter(id__in=cart_list)

            for cart_obj in carts:
                cart_obj.c_is_select = not cart_obj.c_is_select
                cart_obj.save()

            data = {
                'status': 200,
                'msg': 'ok',
                'total_price': get_total_price(self.request)
            }
        elif action == "all":
            carts = Cart.objects.filter(c_user=request.user)

            is_all_select = not carts.filter(c_is_select=False).exists()

            data = {
                'status': 200,
                'msg': 'ok',
                "data": {
                    'title': '购物车',
                    'is_all_select': is_all_select,
                    'total_price': get_total_price(self.request),
                    'carts': CartSerializer(carts, many=True).data,
                }

            }
            return Response(data)
        else:
            data["status"] = status.HTTP_400_BAD_REQUEST
            data["msg"] = "错误的参数"

        return Response(data)


class OrdersAPIView(APIView):
    authentication_classes = (UserTokenAuthentications,)
    permission_classes = (UserLoginPermission,)

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(o_user=request.user)

        data = {
            "status": 200,
            "msg": 'ok',
            "data": {
                "orders": OrderSerializer(orders, many=True).data
            }
        }

        return Response(data)

    def post(self, request, *args, **kwargs):
        carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

        order = Order()

        order.o_user = request.user

        order.o_price = get_total_price(self.request)

        order.save()

        for cart_obj in carts:
            ordergoods = OrderGoods()
            ordergoods.o_order = order
            ordergoods.o_goods_num = cart_obj.c_goods_num
            ordergoods.o_goods = cart_obj.c_goods
            ordergoods.save()
            cart_obj.delete()

        data = {
            "status": 200,
            "msg": 'ok',
            "data": {
                'order_id': order.id
            }

        }

        return Response(data)


class OrderAPIView(APIView):
    authentication_classes = (UserTokenAuthentications,)
    permission_classes = (UserLoginPermission,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        order = Order.objects.filter(o_user=request.user).get(pk=pk)
        data = {
            "status": 200,
            "msg": 'ok',
            "data": {
                "order": OrderSerializer(order).data
            }
        }

        return Response(data)


class AlipayAPIView(APIView):
    authentication_classes = (UserTokenAuthentications,)
    permission_classes = (UserLoginPermission,)

    def get(self, request, *args, **kwargs):

        action = request.query_params.get("action")

        if action == "pay":

            # 构建支付的科幻  AlipayClient
            alipay_client = AliPay(
                appid=ALIPAY_APPID,
                app_notify_url=None,  # 默认回调url
                app_private_key_string=APP_PRIVATE_KEY,
                alipay_public_key_string=ALIPAY_PUBLIC_KEY,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
                sign_type="RSA",  # RSA 或者 RSA2
                debug=False  # 默认False
            )
            # 使用Alipay进行支付请求的发起

            subject = "i9 20核系列 RTX2080"

            # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
            order_string = alipay_client.api_alipay_trade_page_pay(
                out_trade_no="110",
                total_amount=10000,
                subject=subject,
                return_url="http://www.1000phone.com",
                notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
            )

            data = {
                "msg": "ok",
                "status": 200,
                "data": {
                    "pay_url": "https://openapi.alipaydev.com/gateway.do?" + order_string
                }
            }

            return Response(data)

        elif action == "payed":
            order_id = request.query_params.get("orderid")

            order = Order.objects.get(pk=order_id)

            order.o_status = ORDER_STATUS_NOT_SEND

            order.save()

            data = {
                "status": 200,
                'msg': 'payed success'
            }
            return Response(data)

        else:

            data = {
                "msg": "请提供正确的动作",
                "status": 400
            }

            return Response(data)


def get_total_price(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    total = 0

    for cart in carts:
        total += cart.c_goods_num * cart.c_goods.price

    return "{:.2f}".format(total)
