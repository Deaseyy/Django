from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from carts.models import ShoppingCart
from goods.models import Goods
from order.models import OrderInfo
from user.models import User, UserAddress


def place_order(request):
    if request.method == 'GET':
        session_goods = request.session.get('session_goods')  # 从session中获取商品信息
        goods_list = []
        final_price = 0
        if session_goods:
            for g in session_goods:
                goods_id = g[0]
                count = g[1]
                is_select = g[2]
                goods = Goods.objects.filter(id=goods_id).first()
                goods_list.append([goods, count, is_select])
                total_price = count * goods.shop_price  # 小计
                final_price += total_price  # 总价格
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        addrs = UserAddress.objects.filter(user_id=user.id).all()
        return render(request, 'place_order.html', {'goods_list': goods_list, 'final_price': final_price, 'addrs': addrs})


def submit_order(request):
    if request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.filter(username=username).first()
        carts = ShoppingCart.objects.filter(user=user, is_select=1).all()
        final_price = 0
        if carts:
            for cart in carts:
                final_price += cart.nums * cart.goods.shop_price
            order = OrderInfo()
            order.user = user
            order.order_mount = final_price
            order.save()
            return HttpResponseRedirect(reverse('goods:index'))