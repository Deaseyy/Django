from django.urls import path

from carts.views import carts, add_carts, remove_carts, update_carts

urlpatterns = [
    path('carts/', carts, name='carts'),
    path('add_carts/', add_carts, name='add_carts'),
    path('update_carts/', update_carts, name='update_carts'),
    path('remove_carts/', remove_carts, name='remove_carts'),


]