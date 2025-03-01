# from atexit import register
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Category, Product, Cart, Favourite, Order, OrderItem, Payment, HeroSlide, Review, ProductImage
from django.utils.html import format_html
from unfold.admin import ModelAdmin

# admin.site.unregister(Category)
# admin.site.unregister(Product)
# admin.site.unregister(Cart)
# admin.site.unregister(Favourite)

# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_active', 'order', 'created_at', 'image_preview')
#     list_editable = ('is_active', 'order')

#     def image_preview(self, obj):
#         if obj.desktop_image:
#             return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.desktop_image.url)
#         return "-"
#     image_preview.short_description = "Preview"

#  Register HeroSlide model


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ('title', 'subtitle', 'button_text', 'button_link')


class ProductAdmin(ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'vendor', 'product_image', 'quantity',
                    'selling_price', 'discounted_price', 'description', 'status', 'trending', 'featured')


admin.site.register(Product, ProductAdmin)

# Register ProductImage model

admin.site.register(ProductImage)

# Register Review model
admin.site.register(Review)


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
