from django.urls import path

from common import views

urlpatterns = [
    path('credential', views.CredentialView.as_view()),  # 获取临时密钥
]

