
from django.urls import path
from rest_framework.routers import SimpleRouter

from api import views

router = SimpleRouter()


urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('getSmsCode', views.SmsCodeView.as_view()),
    path('photosView', views.PhotosView.as_view()),


]

