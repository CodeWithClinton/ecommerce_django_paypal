from django.urls import path
from . import views

urlpatterns = [
    path('store', views.store, name = 'store'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('updatecart', views.updateCart, name = 'updatecart'),
    path('updatequantity', views.updateQuantity, name = 'updatequantity'),
    path('process-order', views.processOrder, name = 'process-order'),

]