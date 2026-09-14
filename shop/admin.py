from django.contrib import admin
from . models import MyProduct, Order, ContactMessage
# Register your models here.

admin.site.register(MyProduct)
admin.site.register(Order)
admin.site.register(ContactMessage)