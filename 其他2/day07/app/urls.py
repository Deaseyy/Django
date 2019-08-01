
from django.urls import path
from rest_framework.routers import SimpleRouter

from app.views import index, add_art, ArticleView

# 获取路由
router = SimpleRouter()
# 注册资源，/app/article/, /app/article/id/
router.register('article', ArticleView)

urlpatterns = [
    path('index/', index, name='index'),
    path('add_art/', add_art, name='add_art'),
]
# 将rest提供的接口添加到urlpatterns上
urlpatterns += router.urls
