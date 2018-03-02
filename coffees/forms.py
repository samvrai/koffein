from django import forms
from .models import Order, User


class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['date', 'shipping']
        labels = {
            'date': 'Fecha de cierre',
            'shipping': 'Portes'
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'dd/mm/yyyy'},
                                    format='%d-%m-%Y'),
            'shipping': forms.NumberInput(attrs={'class': 'form-control', 'id': 'shipping', 'placeholder': '00,00'})
        }


class OrderUpdate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['date', 'shipping', 'closed']
        labels = {
            'date': 'Fecha de cierre',
            'shipping': 'Portes',
            'closed': 'Cerrado'
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'date', 'placeholder': 'dd/mm/yyyy'},
                                    format='%d-%m-%Y'),
            'shipping': forms.NumberInput(attrs={'class': 'form-control', 'id': 'shipping', 'placeholder': '00,00'}),
            'closed': forms.CheckboxInput(attrs={'class': 'form-control', 'id': 'closed'})
        }


class UserCreate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'paid']
        excluded = ['orders']
        labels = {
            'name': 'Nombre',
            'paid': 'Pagado',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'nombre.apellido'}),
            'paid': forms.HiddenInput(attrs={'id': 'paid', 'value': False, 'hidden': 'true'}),
        }
