from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.product_detail, name="product_detail"),
    path("checkout/", views.checkout, name='checkout'),
    path("checkout/success/<int:order_id>/",
        views.checkout_success,
        name="checkout_success",
    ),  # Added success route
    path("contactus/", views.contactus, name="contactus"),
    path("orders/", views.order_list, name="order_list"),# New route for order list
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('read-messages/', views.read_message, name='read_messages'),  # New route for reading messages
    path('category/<str:category_name>/', views.category_view, name='category_view'),  # New route for category view
    # path('logout/', views.staff_logout, name='logout'),
    # # Only staff members who know this exact URL can reach the login page
    # path('internal-portal-login-x89/', views.staff_login, name='login'),
    path('add-product/', views.add_product, name='add_product'),  # New route for adding products
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),  # New route for editing products
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),  # New route for deleting products
    # API Routes
    path('api/products/', views.PublicProductListAPIView.as_view(), name='api_product_list'),
    path('api/products/<int:id>/', views.PublicProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/orders/create/', views.OrderCreateAPIView.as_view(), name='api_order_create'),  # New API route for creating orders
]
