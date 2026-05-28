from django import forms
from .models import Service, Order, Review, Part, PartType

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
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise forms.ValidationError('Название не может быть пустым')
        return name.strip()
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError('Цена должна быть больше 0')
        return price
    

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'price', 'part_type', 'quantity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название запчасти', 'required': True}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'required': True}),
            'quantity': forms.NumberInput(attrs={'min': 0, 'required': True}),
        }
        labels = {
            'name': 'Название',
            'price': 'Цена (руб.)',
            'part_type': 'Тип запчасти',
            'quantity': 'Количество на складе',
        }    


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'master', 'services', 'parts', 'status']


class OrderClientForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['master', 'services']
        widgets = {
            'services': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'master': 'Выберите мастера',
            'services': 'Выберите услуги',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'placeholder': '1-5',
                'style': 'width: 100px; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ваш отзыв о нашем автосервисе...',
                'style': 'width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;'
            }),
        }
        labels = {
            'author_name': 'Ваше имя',
            'rating': 'Оценка',
            'text': 'Отзыв',
        }