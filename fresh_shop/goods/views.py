from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from carts.models import ShoppingCart
from goods.models import Goods
from user.models import User


def goods_index(request):
    if request.method == 'GET':
        goodss = Goods.objects.filter().all()
        session = request.session.get('session_goods')
        try:
            my_carts = len(session)
        except:
            my_carts = 0
        return render(request, 'index.html', {'goodss': goodss, 'my_carts': my_carts})


def goods_list(request):
    if request.method == 'GET':
        # 我的购物车图标 数量显示
        session = request.session.get('session_goods')
        try:
            my_carts = len(session)
        except:
            my_carts = 0
        # 默认显示所有商品
        goodss = Goods.objects.filter().all()
        # 显示某分类下所有商品
        category = request.GET.get('category')
        if category:
            # 默认分页
            # if request.GET.get('order') == 'default':
            page = request.GET.get('page',1)  # 获取某页数据
            goodss = Goods.objects.filter(category_id=category).all()
            p = Paginator(goodss, 2)  #传入数据,每页显示条数
            goodss = p.page(page)   # 获取指定页的商品 page可以为数字或数字字符
            # 按价格排序后分页      ----------分页还有点问题
            if request.GET.get('order') == 'price':
                page = request.GET.get('page', 1)  # 获取某页数据
                goodss = Goods.objects.filter(category_id=category).order_by('shop_price').all()
                p = Paginator(goodss, 2)  # 传入数据,每页显示条数
                goodss = p.page(page)
        return render(request, 'list.html', {'my_carts': my_carts, 'category':category, 'goodss':goodss})


def goods_detail(request,id):
    if request.is_ajax():
        goods = Goods.objects.filter(id=id).first()
        count = int(request.GET.get('count'))
        total_price = count*goods.shop_price
        print(total_price)
        return JsonResponse({'total_price':total_price})
    if request.method == 'GET':
        # 我的购物车图标 数量显示
        session = request.session.get('session_goods')
        try:
            my_carts = len(session)
        except:
            my_carts = 0
        # 商品详情
        goods = Goods.objects.filter(id=id).first()
        return render(request, 'detail.html', {'goods':goods,'my_carts':my_carts})


def search(request):
    if request.method == 'POST':
        # 我的购物车图标 数量显示
        session = request.session.get('session_goods')
        try:
            my_carts = len(session)
        except:
            my_carts = 0
        # 搜索
        name_keyword = request.POST.get('name_keyword')
        goodss = Goods.objects.filter(name__contains=name_keyword).all()
        if goodss:
            return render(request, 'list.html', {'goodss': goodss, 'my_carts':my_carts})
        else:
            return render(request, 'list.html', {'error': '您查找的商品走丢了!', 'my_carts':my_carts})