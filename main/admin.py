from django.contrib import admin
from .models import Book

from .models import Cart, CartItem, UserProfile

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(UserProfile)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'price')
    search_fields = ('title', 'author', 'genre')

admin.site.register(Book)