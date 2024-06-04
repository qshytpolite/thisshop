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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts',
                             null=True, blank=True)  # Allow for anonymous carts
    # Track session for anonymous users
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        items = Cart.objects.all()
        total = 0
        for item in items:
            if item.product.discounted_price:
                total += item.product.discounted_price * item.product_qty
            else:
                total += item.product.selling_price * item.product_qty
        return total
        # if self.product.discounted_price:
        #     return self.product_qty * self.product.discounted_price
        # else:
        #     return self.product_qty * self.product.selling_price

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

# Order model


class Order(models.Model):
    # Order placed by a user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Date and time order was placed
    placed_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(
        max_digits=10, decimal_places=2)  # Total cost of the order
    # Payment method used (optional)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    # Payment status (pending, completed, failed)
    payment_status = models.CharField(max_length=255, default="pending")
    shipping_address = models.TextField(
        null=True, blank=True)  # Shipping address (optional)
    # Additional fields for tracking and fulfillment can be added

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

# OrderItem model


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')  # Belongs to an order
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)  # Ordered product
    quantity = models.PositiveIntegerField()  # Quantity of the product ordered
    # Price of the product at the time of order
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item: {self.order.pk} - {self.product.name} (x{self.quantity})"
