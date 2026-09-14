from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from shop.models import Order
import json



# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Auto log in upon successful sign up
            messages.success(request, "Account created successfully!")
            return redirect('shop:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'useraccounts/register.html', {'form': form})

def user_logout_view(request):
    logout(request)
    return redirect('shop:index')

@login_required
def profile_view(request):
    user_orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'useraccounts/profile.html', {
        'orders': user_orders
    })
    
@login_required
def user_order_detail(request, order_id):
    # Only allow the user who placed the order to view it
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Safely parse items
    items_data = {}
    if isinstance(order.items, str):
        try:
            items_data = json.loads(order.items)
        except json.JSONDecodeError:
            items_data = {}
    else:
        items_data = order.items

    return render(request, 'useraccounts/user_order_detail.html', {
        'order': order,
        'items_data': items_data,
    })