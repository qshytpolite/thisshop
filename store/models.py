import datetime
import os
from django.contrib.auth.models import User
from django.utils import timezone
# from itertools import product
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
    slug = models.SlugField(unique=True, max_length=150,
                            null=False, blank=False)
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

    # calculate the discount percentage dynamically    @property
    def discount_percentage(self):
        if self.discounted_price and self.selling_price:
            discount = (
                (self.selling_price - self.discounted_price) / self.selling_price) * 100
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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}/5"

# The Cart model represents a product added to a user's cart.


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True
    )
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def item_total(self):
        """Calculate the total cost of the product in the cart."""
        if self.product.discounted_price:
            return self.product.discounted_price * self.product_qty
        return self.product.selling_price * self.product_qty

    # @property
    # def total_cost(self):
    #     """Calculate the total cost of all products in the cart."""
    #     if self.user:
    #         # For authenticated users
    #         items = Cart.objects.filter(user=self.user)
    #     else:
    #         # For anonymous users
    #         items = Cart.objects.filter(session_id=self.session_id)
    #     return items.aggregate(total=Sum('item_total'))['total'] or 0

    def __len__(self):
        """Return the total number of items in the cart."""
        if self.user:
            # For authenticated users
            return Cart.objects.filter(user=self.user).count()
        # For anonymous users
        return Cart.objects.filter(session_id=self.session_id).count()

    class Meta:
        unique_together = (('user', 'product'), ('session_id', 'product'))
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
