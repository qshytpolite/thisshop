from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='index'),
    path('cart', views.cart_page, name="cart"),
    path('fav', views.fav_page, name="fav"),
    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('remove_cart/<str:product_id>', views.remove_cart, name="remove_cart"),
    path('collections', views.collections, name="collections"),
    path('collections/<str:name>', views.collectionsview, name="collections"),
    path('product/<slug:slug>/', views.product_details, name='product_details'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),
#     path('collections/<str:cname>/<str:pname>',
#          views.product_details, name="product_details"),
    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name="add_to_cart"),
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('payment/<int:payment_id>/', views.payment, name='payment'),
    path('paystack-webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('delete-cart-items/', views.delete_cart_items, name='delete_cart_items'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('shop/', views.shop, name='shop'),


]
