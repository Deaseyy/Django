
from django.urls import path
from rest_framework.routers import SimpleRouter

from home.circle import views

router = SimpleRouter()
router.register('news', views.NewsView)

urlpatterns = [
    path('comment', views.CommentView.as_view())
]

urlpatterns += router.urls