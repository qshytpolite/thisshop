import datetime
import os
from django.contrib.auth.models import User
from django.utils import timezone
from itertools import product
from django.db import models
from django.utils.text import slugify
from user.models import User 

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


def getFileName(requset, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join('uploads/', new_filename)

# Create the hero slider model 
class HeroSlide(models.Model):
    image = ProcessedImageField(
        upload_to=getFileName,
        processors=[ResizeToFill(1200, 720)],
        format='JPEG',
        options={'quality': 100},
    )
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

# Create home banner model
# class Banner(models.Model):
#     title = models.CharField(max_length=100, help_text="Title of the banner")
#     subtitle = models.CharField(max_length=100,blank=True, help_text="Optional subtitle")
#     description = models.TextField(blank=True, help_text="Optional description")
#     desktop_image = models.ImageField(upload_to=getFileName, help_text="Upload desktop banner image")
#     mobile_image = models.ImageField(upload_to=getFileName, blank=True, null=True, help_text="Upload mobile banner image (optional)")
#     is_active = models.BooleanField(default=True, help_text="Check to display this banner")
#     order = models.PositiveIntegerField(default=0, help_text="Order in which banners are displayed")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        # Automatically generate slug from name before saving
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=False)
    slug = models.SlugField(unique=True, max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, blank=False)
    product_image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    selling_price = models.FloatField()
    discounted_price = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False)
    trending = models.BooleanField(default=False, help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False, help_text="0-default,1-Featured")

    # calculate the discount percentage dynamically    @property
    def discount_percentage(self):
        if self.discounted_price and self.selling_price:
            discount = ((self.selling_price - self.discounted_price) / self.selling_price) * 100
            return round(discount, 2)  # Round to 2 decimal places
        return 0

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Product, self).save(*args, **kwargs)

# Review model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}/5"

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
