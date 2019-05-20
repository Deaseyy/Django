from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from carts.models import ShoppingCart
from goods.models import Goods
from user.models import User

# final_price = 0  # 定义全局变量
def carts(request):
    if request.method == 'GET':
        session_goods = request.session.get('session_goods')   # 从session中获取商品信息
        goods_list = []
        final_price = 0
        if session_goods:
            for g in session_goods:
                goods_id = g[0]
                count = g[1]
                is_select = g[2]
                goods = Goods.objects.filter(id=goods_id).first()
                goods_list.append([goods,count,is_select])
                total_price = count * goods.shop_price  # 小计
                final_price += total_price    # 总价格
        return render(request, 'carts.html', {'goods_list':goods_list, 'final_price': final_price})


# 修改购物车商品数量
def update_carts(request):
 # 修改购物车小计
 #    if request.is_ajax():
    if request.method == 'GET':
        goods_id = int(request.GET.get('goods_id'))
        count = int(request.GET.get('count'))
        goods = Goods.objects.filter(id=goods_id).first()
        total_price = count * goods.shop_price  # 小计
        # 将修改后的数据存入session
        session_goods = request.session.get('session_goods')   # 从session中获取商品信息
        for g in session_goods:
            if g[0] == goods_id:
                g[1] = count    # 存入修改后的商品数量
                request.session['session_goods'] = session_goods

        return JsonResponse({'total_price': total_price})


# 添加商品到购物车
def add_carts(request):
    if request.method == 'GET':
        goods_id = int(request.GET.get('id'))
        count = int(request.GET.get('count'))
        is_select = 0
        # 添加商品到session
        session_goods = request.session.get('session_goods')
        if not session_goods:
            session_goods = []
            request.session['is_sync'] = 0
        else:
            for g in session_goods:
                if g[0] == goods_id:
                    g[1] += count
                    request.session['session_goods'] = session_goods
                    return JsonResponse({'success': '成功添加到购物车'})
        session_goods.append([goods_id, count, is_select])
        request.session['session_goods'] = session_goods
        return JsonResponse({'success': '成功添加到购物车'})


# 删除购物车商品
def remove_carts(request):
    if request.is_ajax():
        goods_id = int(request.GET.get('goods_id'))
        final_price = int(request.GET.get('final_price'))
        goods = Goods.objects.filter(id=goods_id).first()
        session_goods = request.session.get('session_goods')

        for g in session_goods:
            if g[0] == goods_id:
                session_goods.remove(g)     # 删除session中的数据
                request.session['session_goods']=session_goods
                carts = ShoppingCart.objects.filter(goods_id=goods_id).first()
                carts.delete()    # 删除数据库数据
                total_price = goods.shop_price * g[1]
                final_price -= total_price
        return JsonResponse({'success': '删除ok', 'final_price': final_price})





