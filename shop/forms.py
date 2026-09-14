from django import forms
from .models import Order, ContactMessage, MyProduct

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' John@gmail.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message here...', 'rows': 5}),
        } 


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone_num', 'address', 'city', 'state', 'zip_code', 'items', 'total_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'phone_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 000-0000'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Commerce St'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'New York'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NY'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10001'}),
            'items': forms.HiddenInput(attrs={'id': 'items'}),
            'total_price': forms.HiddenInput(attrs={'id': 'total_price'}),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = MyProduct
        fields = ['title', 'price','dis_price', 'image', 'category', 'description']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dis_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }