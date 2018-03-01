from django import forms
from .models import Order


class SearchForm(forms.Form):
    username = forms.CharField(help_text='nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))


class OrderCreate(forms.ModelForm):
    model = Order

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
    model = Order

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