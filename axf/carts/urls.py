from django.urls import path
from rest_framework.routers import SimpleRouter

from carts.views import CartView

router = SimpleRouter()
router.register('cart', CartView)


urlpatterns = [


]
urlpatterns += router.urls