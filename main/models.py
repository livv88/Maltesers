
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

class Book(models.Model):
    choices = {
        "shipping_cost": [
            ('Free Shipping', 'Free Shipping'),
            ('Standard Shipping', 'Standard Shipping'),
            ('Express Shipping', 'Express Shipping'),
            ('International Shipping', 'International Shipping'),
            ('Out of stock', 'Out of Stock'),
            ('Preorder', 'Preorder'),
        ]
    }

    image = models.ImageField(upload_to='images/', null=True, blank=False)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    reviews = models.CharField(default=0)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=100, default='English')
    publication_date = models.CharField(max_length=100, default='Unknown')
    paperback = models.CharField(max_length=100, default='Unavailable')
    hardcover = models.CharField(max_length=100, default='Unavailable')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    shipping_cost = models.CharField(max_length=100, default='Free Shipping', choices=choices['shipping_cost'])

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)