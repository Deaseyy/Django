from django.urls.conf import path,re_path
from rest_framework_jwt.views import obtain_jwt_token
from . import views
urlpatterns = [
    path(r'login/', obtain_jwt_token ),
    path(r'register/', views.UserAPIView.as_view() ),
    path(r'captcha/', views.CaptchaAPIView.as_view() ),
    re_path(r'sms/(?P<mobile>1[3-9]\d{9})/', views.SMSAPIView.as_view() ),
    re_path(r'(?P<pk>\d+)/orders/',views.UserOrderAPIView.as_view()),
]