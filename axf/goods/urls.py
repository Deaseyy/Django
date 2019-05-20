from django.urls import path
from rest_framework.routers import SimpleRouter

from goods.views import home, FoodTypeView, MarketView, Home

router = SimpleRouter()
router.register('foodtype', FoodTypeView)  # 只需用到foodtype一个资源
router.register('market', MarketView)      # 只需用到 goods一个资源

urlpatterns = [
    # function形式,使用api_view装饰器
    path('home/', home),   # 不只一个资源模型,使用api_view装饰器,或继承API_View
    # # 类形式,继承APIView的形式,官网推荐
    path('home2/', Home.as_view())
]

urlpatterns += router.urls