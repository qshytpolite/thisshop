# from atexit import register
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Catagory, Product, Cart, Favourite

from unfold.admin import ModelAdmin

# admin.site.unregister(Catagory)
# admin.site.unregister(Product)
# admin.site.unregister(Cart)
# admin.site.unregister(Favourite)


class ProductAdmin(ModelAdmin):
    list_display = ('name', 'vendor', 'product_image', 'quantity',
                    'selling_price', 'discounted_price', 'description', 'status')


admin.site.register(Product, ProductAdmin)


class CatagoryAdmin(ModelAdmin):
    list_display = ('name', 'image', 'description', 'status')


admin.site.register(Catagory, CatagoryAdmin)


class CartAdmin(ModelAdmin):
    # list_display = ('user', 'product', 'product_qty', 'created_at')
    pass


admin.site.register(Cart, CartAdmin)


class FavouriteAdmin(ModelAdmin):
    list_display = ('user', 'product')


admin.site.register(Favourite, FavouriteAdmin)

"""
class CategoryAdmin(admin.ModelAdmin):
  list_display = ('name', 'image', 'description')
admin.site.register(Catagory,CategoryAdmin)
"""

# admin.site.register(Catagory)
# admin.site.register(Product)
# admin.site.register(Cart)
# admin.site.register(Favourite)
