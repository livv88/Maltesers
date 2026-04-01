from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('api/book/<int:book_id>/', views.get_book_details, name='get_book_details'),
    path('api/cart/add/', views.api_cart_add, name='api_cart_add'),
    path('api/cart/remove/', views.api_cart_remove, name='api_cart_remove'),
    path('api/cart/update/', views.api_cart_update, name='api_cart_update'),
    path('api/cart/get/', views.api_cart_get, name='api_cart_get'),
]