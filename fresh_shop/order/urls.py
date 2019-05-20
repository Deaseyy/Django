from django.urls import path

from order.views import place_order, submit_order

urlpatterns = [
    path('place_order/', place_order, name='place_order'),
    path('submit_order/', submit_order, name='submit_order')
]