from django.urls import path
from rest_framework.routers import SimpleRouter

from user.views import UserView


router = SimpleRouter()
router.register('auth',UserView)


urlpatterns = [

]

urlpatterns += router.urls