from django import forms
from .models import Order, CoffeeUser, Coffee


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


class UserCreate(forms.Form):
    model = CoffeeUser

    class Meta:
        CHOICES = Coffee.objects.defer('name').all()
        fields = ['coffee', 'quantity'],
        labels = {
            'coffee': 'Café',
            'quantity': 'Cantidad'
        },
        widgets = {
            'coffee': forms.ChoiceField(choices=CHOICES),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'quantity', 'placeholder': '00'})
        }

    def __init__(self, *args, **kwargs):
        self.order = kwargs.pop('order')
        super(UserCreate, self).__init__(*args, **kwargs)
