import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from shop.models import MyProduct, Order, ContactMessage  #[cite: 5]
from shop.forms import OrderForm, ContactForm  #[cite: 4]

User = get_user_model()


class ShopModelTests(TestCase):
    """Verifies database models, default values, and string representations."""

    def setUp(self):
        self.product = MyProduct.objects.create(
            title="Noise Cancelling Headphones",
            price=99.99,
            dis_price=129.99,
            category="electronics",
            description="High fidelity wireless headphones.",
        )  #[cite: 5]

    def test_product_str(self):
        """Ensure MyProduct __str__ returns the product title."""
        self.assertEqual(str(self.product), "Noise Cancelling Headphones")  #[cite: 5]

    def test_order_creation_and_str(self):
        """Ensure Order records save properly with default pending status."""
        order = Order.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            phone_num="+15551234567",
            address="456 Elm St",
            city="New York",
            state="NY",
            zip_code="10001",
            items=json.dumps({"1": [2, "Noise Cancelling Headphones", 99.99]}),
            total_price=199.98,
        )  #[cite: 5]
        self.assertEqual(order.status, "Pending")  #[cite: 5]
        self.assertEqual(str(order), f"Order #{order.id} - Jane Doe")  #[cite: 5]


class ShopFormTests(TestCase):
    """Verifies form validation logic and required fields."""

    def test_order_form_valid(self):
        form_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone_num": "+15551234567",
            "address": "456 Elm St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "items": '{"1": [1, "Test Item", 10.0]}',
            "total_price": "10.00",
        }  #[cite: 4]
        form = OrderForm(data=form_data)  #[cite: 4]
        self.assertTrue(form.is_valid(), form.errors)

    def test_order_form_missing_required_fields(self):
        form = OrderForm(data={"name": "Jane Doe"})  #[cite: 4]
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)  #[cite: 4]
        self.assertIn("address", form.errors)  #[cite: 4]

    def test_contact_form_valid(self):
        form_data = {
            "name": "Alex Smith",
            "email": "alex@example.com",
            "subject": "Delivery Question",
            "message": "When will my item arrive?",
        }  #[cite: 4]
        form = ContactForm(data=form_data)  #[cite: 4]
        self.assertTrue(form.is_valid(), form.errors)


class ShopViewTests(TestCase):
    """Verifies public store views, search filters, pagination, and order submissions."""

    def setUp(self):
        self.client = Client()
        # Seed 6 products to test pagination (configured at 4 items per page)
        for i in range(1, 7):
            MyProduct.objects.create(
                title=f"Gadget {i}",
                price=10.00 * i,
                dis_price=12.00 * i,
                category="electronics" if i % 2 == 0 else "clothing",
                description=f"Description for item {i}",
            )  #[cite: 5, 7]

    def test_index_view_loads_and_paginates(self):
        """Index page should return status 200 and paginate 4 items on page 1."""
        response = self.client.get(reverse("shop:index"))  #[cite: 6]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "shop/index.html")  #[cite: 7]
        # Paginator splits 6 products into 4 on the first page
        self.assertEqual(len(response.context["products_obj"]), 4)  #[cite: 7]

    def test_index_search_filter(self):
        """Searching by item_name query param filters the queryset properly."""
        response = self.client.get(reverse("shop:index"), {"item_name": "Gadget 1"})  #[cite: 6, 7]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products_obj"]), 1)  #[cite: 7]

    def test_product_detail_view(self):
        product = MyProduct.objects.first()
        response = self.client.get(reverse("shop:product_detail", args=[product.id]))  #[cite: 6]
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.title)  #[cite: 7]

    def test_checkout_post_creates_order(self):
        """Submitting a valid checkout form creates a new Order record and redirects."""
        payload = {
            "name": "Customer One",
            "email": "customer@example.com",
            "phone_num": "555-0100",
            "address": "123 Main St",
            "city": "Boston",
            "state": "MA",
            "zip_code": "02108",
            "items": '{"1": [1, "Gadget 1", 10.0]}',
            "total_price": "10.00",
        }  #[cite: 4, 5]
        response = self.client.post(reverse("shop:checkout"), payload)  #[cite: 6, 7]
        
        self.assertEqual(Order.objects.count(), 1)  #[cite: 7]
        new_order = Order.objects.first()
        self.assertRedirects(response, reverse("shop:checkout_success", args=[new_order.id]))  #[cite: 6, 7]


class StaffAccessControlTests(TestCase):
    """Verifies that sensitive management views are guarded by @staff_member_required."""

    def setUp(self):
        self.client = Client()
        self.regular_user = User.objects.create_user(
            username="shopper", email="shopper@test.com", password="password123"
        )
        self.staff_user = User.objects.create_user(
            username="manager", email="manager@test.com", password="password123", is_staff=True
        )

    def test_order_list_requires_staff(self):
        """Anonymous or regular users should be redirected to the admin login page."""
        response = self.client.get(reverse("shop:order_list"))  #[cite: 6]
        self.assertEqual(response.status_code, 302)
        self.assertIn("admin/login", response.url)  #[cite: 7]

        # Regular authenticated user is also blocked
        self.client.login(username="shopper", password="password123")
        response = self.client.get(reverse("shop:order_list"))  #[cite: 6]
        self.assertEqual(response.status_code, 302)
        self.assertIn("admin/login", response.url)  #[cite: 7]

    def test_order_list_accessible_by_staff(self):
        """Staff members should get a 200 OK status."""
        self.client.login(username="manager", password="password123")
        response = self.client.get(reverse("shop:order_list"))  #[cite: 6]
        self.assertEqual(response.status_code, 200)  #[cite: 7]


class ShopAPITests(APITestCase):
    """Verifies DRF public and order creation endpoints."""

    def setUp(self):
        self.product = MyProduct.objects.create(
            title="Smart Watch",
            price=199.99,
            dis_price=249.99,
            category="electronics",
            description="Tracks heart rate and fitness.",
        )  #[cite: 5]

    def test_public_product_list_api(self):
        url = reverse("shop:api_product_list")  #[cite: 6]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  #[cite: 7]
        self.assertGreaterEqual(len(response.data), 1)  #[cite: 7]

    def test_public_product_detail_api(self):
        url = reverse("shop:api_product_detail", args=[self.product.id])  #[cite: 6]
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  #[cite: 7]
        self.assertEqual(response.data["title"], "Smart Watch")  #[cite: 5, 7]
