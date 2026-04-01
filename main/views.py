from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Cart, CartItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

def landing(request):
    return render(request, 'main/landing.html')

from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    books = Book.objects.all()
    sections = {
        'MyBooks': books[15:20],
        'BestSellers': books[:5],
        'WeeklySeries': books[20:25],
        'Horror': books[5:10],
        'Romance': books[10:15],
        'International': books[25:30],
    }
    login_form = CustomAuthenticationForm()
    register_form = CustomUserCreationForm()
    login_error = None
    register_error = None

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data.get('username'),
                    password=login_form.cleaned_data.get('password')
                )
                if user is not None:
                    auth_login(request, user)
                    return redirect('home')
                else:
                    login_error = 'Invalid username or password.'
            else:   
                login_error = 'Invalid login form.'
        elif 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                # Save extra fields to UserProfile
                from .models import UserProfile
                phone = register_form.cleaned_data.get('phone', '')
                address = register_form.cleaned_data.get('address', '')
                UserProfile.objects.create(user=user, phone=phone, address=address)
                print(f"DEBUG: Created user {user.username} (ID: {user.id}) with profile.")
                auth_login(request, user)
                return redirect('home')
            else:
                print(f"DEBUG: Registration errors: {register_form.errors}")
                register_error = 'Registration failed. Please check the form.'
        elif 'logout' in request.POST:
            from django.contrib.auth import logout
            logout(request)
            return redirect('home')

    context = sections.copy()
    context.update({
        'login_form': login_form,
        'register_form': register_form,
        'login_error': login_error,
        'register_error': register_error,
    })
    return render(request, 'main/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def get_book_details(request, book_id):
    book = Book.objects.get(id=book_id)
    data = {
        'title': book.title,
        'author': book.author,
        'rating': book.rating,
        'genre': book.genre,
        'pages': book.pages,
        'language': book.language,
        'publication_date': book.publication_date,
        'paperback': book.paperback,
        'hardcover': book.hardcover,
        'price': book.price,
        'discount': book.discount,
        'shipping_cost': book.shipping_cost,
        'reviews': book.reviews,
        'description': book.description,
        'image': book.image.url if book.image else None,
    }
    return JsonResponse(data)

@csrf_exempt
@login_required
def api_cart_add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)
        book = Book.objects.get(id=book_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity
        item.save()
        return JsonResponse({'success': True, 'item_id': item.id, 'quantity': item.quantity})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def api_cart_remove(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def api_cart_update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = data.get('quantity')
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.quantity = quantity
            item.save()
            return JsonResponse({'success': True, 'quantity': item.quantity})
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_cart_get(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    result = []
    for item in items:
        result.append({
            'item_id': item.id,
            'book_id': item.book.id,
            'title': item.book.title,
            'author': item.book.author,
            'image': item.book.image.url if item.book.image else '',
            'discount': str(item.book.discount),
            'price': str(item.book.price),
            'quantity': item.quantity,
        })
    return JsonResponse({'items': result})