from django.shortcuts import render,redirect,get_object_or_404
from .models import MyProduct,Order,ContactMessage,Wishlist
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import ContactForm,OrderForm,ProductForm,OrderShippingForm
import json
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic.edit import DeleteView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from useraccounts.forms import PostPurchaseRegisterForm
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

User = get_user_model()



# Create your views here.
def index(request):
    products_obj = MyProduct.objects.all()
    
    #search functionality
    item_name = request.GET.get("item_name")
    if item_name != "" and item_name is not None:
        products_obj = products_obj.filter(title__icontains=item_name)

    #paginator functionality
    paginator = Paginator(products_obj, 4) # Shows 4 products per page.
    page_number = request.GET.get("page")
    products_obj = paginator.get_page(page_number)
    
    # retrieve wishlist IDs for logged-in user to highlight saved hearts
    user_wishlist_ids = set()
    if request.user.is_authenticated:
        user_wishlist_ids = set(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    
    return render(request, "shop/index.html", {
        "products_obj": products_obj,
        "user_wishlist_ids": user_wishlist_ids
    })

def product_detail(request, id):
    product = get_object_or_404(MyProduct, id=id)
    return render(request, "shop/product_detail.html", {"product":product})

def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Link user automatically if authenticated
            if request.user.is_authenticated:
                order.user = request.user
                
            order.save()
            return redirect("shop:checkout_success", order_id=order.id)
    else:
        # Pre-fill name and email for logged-in users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'email': request.user.email,
                'name': request.user.first_name or request.user.username,
            }
        form = OrderForm(initial=initial_data)

    return render(request, "shop/checkout.html", {"form": form})
    
def checkout_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = PostPurchaseRegisterForm()
    
    if request.method == "POST":
        form = PostPurchaseRegisterForm(request.POST)
        if form.is_valid():
            email = order.email
            password = form.cleaned_data['password']

            # Check if an account with this email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists. Please log in.")
                return redirect('useraccounts:login')

            # Create a new user account using order details
            username = email.split('@')[0]  # Or generate a unique username
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=order.name
            )

            # Link the order to the new user and save
            order.user = user
            order.save()

            # Automatically log the user in
            login(request, user)
            messages.success(request, "Your account has been created! Your order is now saved to your account.")
            return redirect('shop:checkout_success', order_id=order.id)

    return render(request, "shop/checkout_success.html", {
        "order": order,
        "form": form
    })


def contactus(request):
    success_msg = None
    if request.method == "POST":
        contactform = ContactForm(request.POST)

        if contactform.is_valid():
            contactform.save()  # Save the form data to the database

            # Message delivery or database logic here...

            success_msg = (
                f"Thank you {contactform.cleaned_data['name']}, your message has been sent successfully!"
            )
            contactform = ContactForm()  # Clear form on success
    else:
        contactform = ContactForm()

    return render(
        request, "shop/contact.html", {"contactform": contactform, "success_msg": success_msg}
    )
    
# def order_list(request):
#     orders = Order.objects.all().order_by('-created_at')  # Fetch all orders, most recent first
#     return render(request, "shop/order_list.html", {"orders": orders})

@staff_member_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Search by Order ID, Name, or Email
    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            models.Q(id__icontains=search_query) |
            models.Q(name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
        
    # Filter by Status
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, "shop/order_list.html", {
        "orders": orders,
        "search_query": search_query,
        "status_filter": status_filter,
        "status_choices": Order.STATUS_CHOICES,
    })
    
@staff_member_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)  #[cite: 12]
    shipping_form = OrderShippingForm(instance=order)

    # Process Form Submissions
    if request.method == "POST":
        action = request.POST.get("action")

        # 1. Update Order Status
        if action == "update_status":
            new_status = request.POST.get("status")  #[cite: 12]
            if new_status in dict(Order.STATUS_CHOICES):  #[cite: 12]
                order.status = new_status  #[cite: 12]
                order.save()  #[cite: 12]
                messages.success(request, f"Order #{order.id} status updated to '{new_status}'.")  #[cite: 12]
                return redirect('shop:order_detail', order_id=order.id)  #[cite: 12]

        # 2. Update Customer & Shipping Information
        elif action == "update_shipping":
            shipping_form = OrderShippingForm(request.POST, instance=order)
            if shipping_form.is_valid():
                shipping_form.save()
                messages.success(request, f"Shipping and customer details for Order #{order.id} updated successfully.")
                return redirect('shop:order_detail', order_id=order.id)
            else:
                messages.error(request, "Failed to update shipping details. Please correct the form errors.")

    # Parse items JSON safely
    items_data = {}  #[cite: 12]
    if isinstance(order.items, str):  #[cite: 12]
        try:
            items_data = json.loads(order.items)  #[cite: 12]
        except json.JSONDecodeError:  #[cite: 12]
            items_data = {}  #[cite: 12]
    else:
        items_data = order.items  #[cite: 12]

    return render(request, 'shop/order_detail.html', {
        'order': order,  #[cite: 12]
        'items_data': items_data,  #[cite: 12]
        'status_choices': Order.STATUS_CHOICES,  #[cite: 12]
        'shipping_form': shipping_form,
    })
        
@staff_member_required
def read_message(request):
    messages = ContactMessage.objects.all().order_by('-created_at')  # Fetch all messages, most recent first
    return render(request, "shop/read_message.html", {"messages": messages})

def category_view(request, category_name):
    product_obj = MyProduct.objects.filter(category__iexact=category_name)    
    return render(request, "shop/category.html", {"product_obj": product_obj, "category_name": category_name})

# def staff_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
            
#             # Reject non-staff accounts
#             if not user.is_staff:
#                 messages.error(request, "Access restricted to authorized staff only.")
#                 return render(request, 'shop/login.html', {'form': form})
#             login(request, user)
#             return redirect('shop:order_list')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'shop/login.html', {'form': form})


# def staff_logout(request):
#     logout(request)
#     return redirect('shop:index')


@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully.")
            return redirect('shop:index')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Add New Product'})
    
@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(MyProduct, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('shop:product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'title': 'Edit Product'})

@staff_member_required
def delete_product(request,product_id):
    product = get_object_or_404(MyProduct, id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('shop:index')
    return redirect('shop:product_detail', id=product.id)

import ast
import json

def parse_order_items(raw_items):
    """Safely decodes both valid JSON strings and Python literal dicts/lists."""
    if not raw_items:
        return {}
    if isinstance(raw_items, (dict, list)):
        return raw_items
    try:
        return json.loads(raw_items)
    except (json.JSONDecodeError, TypeError):
        try:
            return ast.literal_eval(raw_items)
        except (ValueError, SyntaxError):
            return {}
        
@login_required
def wishlist_view(request):
    """Renders the saved items collection for the logged-in user."""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, "shop/wishlist.html", {"wishlist_items": wishlist_items})

@login_required
def toggle_wishlist(request, product_id):
    """AJAX endpoint to toggle a product into or out of the user's wishlist."""
    if request.method == "POST":
        product = get_object_or_404(MyProduct, id=product_id)
        wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

        if wishlist_item:
            wishlist_item.delete()
            saved = False
            message = f"{product.title} removed from saved items."
        else:
            Wishlist.objects.create(user=request.user, product=product)
            saved = True
            message = f"{product.title} added to saved items."

        total_count = Wishlist.objects.filter(user=request.user).count()
        return JsonResponse({
            "saved": saved,
            "message": message,
            "total_count": total_count
        })

    return JsonResponse({"error": "Invalid request method"}, status=400)

# # Public API: List all products or create a new product (Admin/Staff only)
# class ProductListCreateAPIView(ListCreateAPIView):
#     queryset = MyProduct.objects.all()
#     serializer_class = ProductSerializer

#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [IsAdminUser()]
#         return [AllowAny()]

# # Public API: Retrieve, update, or delete a single product
# class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = MyProduct.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'

#     def get_permissions(self):
#         if self.request.method in ['PUT', 'PATCH', 'DELETE']:
#             return [IsAdminUser()]
#         return [AllowAny()]

# ONLY allows GET requests to list all products
class PublicProductListAPIView(ListAPIView):
    queryset = MyProduct.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'category', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# ONLY allows GET requests to view a single product
class PublicProductDetailAPIView(RetrieveAPIView):
    queryset = MyProduct.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]
    
class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Allow anyone to create an order
    
    
