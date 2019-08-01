from django.conf.urls import url

from App import views

urlpatterns = [
    # 首页地址
    url(r'^home/', views.MainAPIView.as_view()),
    # 闪购超市
    url(r'^foodtypes/', views.FoodTypeAPIView.as_view()),
    url(r'^market/', views.MarketAPIView.as_view()),
    # 用户
    url(r'^users/', views.AXFUserAPIView.as_view()),
    # 阿里支付
    url(r'^alipay/', views.AlipayAPIView.as_view()),
    # 购物车
    url(r'^carts/', views.CartAPIView.as_view()),
    # 订单
    url(r'^orders/$', views.OrdersAPIView.as_view()),
    url(r'^orders/(?P<pk>\d+)/', views.OrderAPIView.as_view()),
]
