from django.contrib.auth.models import User
from itertools import product
from django.db import models
from user.models import User
import datetime
import os


def getFileName(requset, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)


class Catagory(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    vendor = models.CharField(max_length=150, blank=False)
    product_image = models.ImageField(
        upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    trending = models.BooleanField(
        default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_total(self):
        if self.product.discounted_price:
            return self.product.discounted_price * self.product_qty
        else:
            return self.product.selling_price * self.product_qty

    @property
    def total_cost(self):
        items = Cart.objects.all()
        total = 0
        for item in items:
            total += item.item_total
        return total

    def __len__(self):
        # count all items in the cart
        return self.product_qty

    class Meta:
        # Unique constraint to ensure one item per product in a cart
        unique_together = (('user', 'product'),)
        # Ordering by creation date for retrieval
        ordering = ['-created_at']


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
