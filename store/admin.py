# from atexit import register
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Cart, Favourite, Order, OrderItem, Payment

from unfold.admin import ModelAdmin

# admin.site.unregister(Category)
# admin.site.unregister(Product)
# admin.site.unregister(Cart)
# admin.site.unregister(Favourite)


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'vendor', 'product_image', 'quantity',
                    'selling_price', 'discounted_price', 'description', 'status', 'trending', 'featured')


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'image', 'description', 'status')


admin.site.register(Category, CategoryAdmin)


class CartAdmin(ModelAdmin):
    list_display = ('user', 'product', 'product_qty', 'created_at')


admin.site.register(Cart, CartAdmin)


class FavouriteAdmin(ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Favourite, FavouriteAdmin)


class OrderAdmin(ModelAdmin):
    # list_display = ('user', 'status', 'created_at')
    pass


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(ModelAdmin):
    # list_display = ('order', 'product', 'quantity')
    pass


admin.site.register(OrderItem, OrderItemAdmin)


class PaymentAdmin(ModelAdmin):
    pass


admin.site.register(Payment, PaymentAdmin)

"""
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'image', 'description')
admin.site.register(Category,CategoryAdmin)
"""

# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(Favourite)
