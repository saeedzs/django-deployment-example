from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

class MyProduct(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    dis_price = models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', default="default.png")

    def __str__(self):
        return self.title
    

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    # Optional link to User (supports guest checkouts and preserves history)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    items = models.CharField(max_length=1000)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_num = models.CharField(null=False, blank=False, max_length= 15, default="")
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=100)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} - {self.name}"
    
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"