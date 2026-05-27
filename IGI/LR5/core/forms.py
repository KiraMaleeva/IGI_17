from django import forms
from .models import Service, Order, Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'service_type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название услуги', 'required': True}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'required': True}),
        }
        labels = {
            'name': 'Название',
            'price': 'Цена (руб.)',
            'service_type': 'Тип услуги',
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'master', 'services', 'status']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }