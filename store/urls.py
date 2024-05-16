from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='index'),
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('collections/<str:cname>/<str:pname>',
         views.product_details, name="product_details"),
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
]
