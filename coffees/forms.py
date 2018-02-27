from django import forms
from .models import Order


class SearchForm(forms.Form):
    username = forms.CharField(help_text='nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))


class OrderForm(forms.ModelForm):
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


class UpdateUserForm(forms.Form):
    user = forms.CharField()
