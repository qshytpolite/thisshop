import datetime
import os
from django.contrib.auth.models import User
from django.utils import timezone
from itertools import product
from django.db import models
from user.models import User


def getFileName(requset, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    vendor = models.CharField(max_length=150, blank=False)
    product_image = models.ImageField(
        upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False)
    trending = models.BooleanField(
        default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(
        default=False, help_text="0-default,1-Featured")

    def __str__(self):
        return self.name


# The Cart model represents a product added to a user's cart.
# It has a foreign key relationship with the User model and the Product model.
# The session_id field is used to store the session ID of the user's cart.
# The product_qty field represents the quantity of the product added to the cart.
# The created_at field represents the date and time when the product was added to the cart.
class Cart(models.Model):
    # Foreign key to the User model, used to represent the user who added the product to the cart.
    # The related_name argument is used to define a reverse relationship from the User model.
    # The null and blank arguments are used to allow null values and blank values for the field.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    # CharField to store the session ID of the user's cart.
    # The null and blank arguments are used to allow null values and blank values for the field.
    session_id = models.CharField(max_length=255, null=True, blank=True)
    # Foreign key to the Product model, used to represent the product added to the cart.
    # The on_delete argument is used to specify the action to be taken when the related product is deleted.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # IntegerField to represent the quantity of the product added to the cart.
    # The default argument is used to set the default value of the field.
    product_qty = models.IntegerField(default=0)
    # DateTimeField to represent the date and time when the product was added to the cart.
    # The auto_now_add argument is used to automatically set the field to the current date and time when the object is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # Property method to calculate the total cost of the product in the cart.
    # It multiplies the product's discounted price (if available) by the product quantity.
    # Otherwise, it multiplies the product's selling price by the product quantity.
    @property
    def item_total(self):
        if self.product.discounted_price:
            return self.product.discounted_price * self.product_qty
        else:
            return self.product.selling_price * self.product_qty

    # Property method to calculate the total cost of all products in the cart.
    # It retrieves all items in the cart for the user and calculates the total cost using the item_total property method.
    @property
    def total_cost(self):
        items = Cart.objects.filter(user=self.user)
        total = 0
        for item in items:
            total += item.item_total
        return total

    # Magic method to provide the length of the cart.
    # It returns the product quantity in the cart.
    def __len__(self):
        # count all items in the cart
        return self.product_qty

    class Meta:
        # Meta class is used to define metadata for the model.
        # The unique_together argument is used to specify a unique constraint on the user and product fields.
        # The ordering argument is used to specify the order in which objects are retrieved.
        unique_together = (('user', 'product'),)
        ordering = ['-created_at']


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # number of favourite products for a user
    @property
    def fav_count(self):
        return Favourite.objects.filter(user=self.user).count()


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

# Payment Models


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.reference} - {self.status}"
