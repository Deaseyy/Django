import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# 登陆校验中间件
from carts.models import ShoppingCart
from user.models import User


class UserLoginMiddleware(MiddlewareMixin):
    # 请求之前执行该函数
    def process_request(self,request):
        not_need_check =  ['/user/login/', '/user/register/', '/user/logout/',
                           '/goods/(.*)', '/carts/(.*)',]
        path = request.path  #获取请求地址
        # if path in not_need_check:  # <转换器匹配>
        #     return None
        for not_path in not_need_check:
            if re.match(not_path,path):  # 正则匹配当前路由是否需要验证
                return None
        username = request.session.get('username')
        if not username:
            return HttpResponseRedirect(reverse('user:login'))
        # session存入的是user_id,需要将用户对象绑定到request.user,才能全局使用
        # user = User.objects.get(pk=user_id)
        # request.user = user


# 登陆时同步购物车数据中间件
class AddCartsMiddleware(MiddlewareMixin):
    def process_response(self, request,response):
        username = request.session.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            # 获取购物车中所有goods_id
            goods_id_list = ShoppingCart.objects.filter(user_id=user.id).all().values('goods_id') # 存放形式:[{},{}]
            goods_ids = []
            for goods_id_dict in goods_id_list:   # 列表套内了一个字典
                goods_ids.append(goods_id_dict['goods_id'])

            session_goods = request.session.get('session_goods')
            if session_goods:   # 是否存在session_goods
                # session数据同步到购物车
                for g in session_goods:
                    if g[0] in goods_ids:
                        carts = ShoppingCart.objects.filter(user_id=user.id,goods_id=g[0]).first()
                        if request.session.get('is_sync') == 0:
                            carts.nums += g[1]  # 登陆后第一次同步: session数量叠加到数据库
                        else:
                            carts.nums = g[1]  # # 之后同步,将session的商品num替换数据库的num
                        carts.save()
                    else:
                        carts = ShoppingCart()
                        carts.goods_id = g[0]
                        carts.nums = g[1]
                        carts.is_select = 1
                        carts.user_id = user.id
                        carts.save()
            request.session['is_sync'] = 1  # 第一次同步后:将状态置1
            # 购物车同步到session
            cartss = ShoppingCart.objects.filter(user_id=user.id).all()  # 获取购物车所有数据
            session_goods = []
            for carts in cartss:
                goods_id = carts.goods_id
                count = carts.nums
                is_select = carts.is_select
                session_goods.append([goods_id, count, is_select])
                request.session['session_goods'] = session_goods
        return response









                # else:   # 第一次之后进来
                #     for g in session_goods:
                #         if g[0] in goods_ids:
                #             carts = ShoppingCart.objects.filter(user_id=user.id,goods_id=g[0]).first()
                #             carts.nums = g[1]   # 第二次进来,将session的商品num替换数据库的num
                #             carts.save()
                #         else:
                #             carts = ShoppingCart()
                #             carts.goods_id = g[0]
                #             carts.nums = g[1]
                #             carts.is_select = 1
                #             carts.user_id = user.id
                #             carts.save()
                # # 购物车同步到session
                # cartss = ShoppingCart.objects.filter(user_id=user.id).all() # 获取购物车所有数据
                # session_goods = []
                # for carts in cartss:
                #     goods_id = carts.goods_id
                #     count = carts.nums
                #     is_select = carts.is_select
                #     session_goods.append([goods_id, count, is_select])
                #     request.session['session_goods'] = session_goods

