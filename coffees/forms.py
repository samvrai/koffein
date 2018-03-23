from django import forms
from .models import Order, User, Coffee, CoffeeUserOrder, CoffeeUserOrderQuantity


class OrderCreateForm(forms.ModelForm):
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


class OrderUpdateForm(forms.ModelForm):
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


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']
        excluded = ['orders']
        labels = {
            'name': 'Nombre',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'nombre.apellido'}),
        }


class CoffeeSelectorForm(forms.Form):
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        user = kwargs.pop('user', None)

        super(CoffeeSelectorForm, self).__init__(*args, **kwargs)

        coffee_list = CoffeeUserOrder.objects.get(order=order, user=user)

        for coffee in Coffee.objects.all():
            if coffee in coffee_list.coffees.all():
                checked = True
            else:
                checked = False
            self.fields['coffee_' + str(coffee.id)] = forms.BooleanField(required=False,
                                                                         label=coffee.name,
                                                                         widget=forms.CheckboxInput(
                                                                             attrs={'class': 'form-check-input',
                                                                                    'checked': checked}))


class UserUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        order = kwargs.pop('order', None)
        user = kwargs.pop('user', None)

        super(UserUpdateForm, self).__init__(*args, **kwargs)

        cuo = CoffeeUserOrder.objects.get(order=order, user=user)
        coffees = CoffeeUserOrderQuantity.objects.filter(cuo=cuo)

        for coffee in coffees:
            self.fields['coffee_' + str(coffee.coffee.id)] = forms.IntegerField(required=True,
                                                                                label=coffee.coffee.name,
                                                                                initial=coffee.quantity,
                                                                                widget=forms.NumberInput(
                                                                                    attrs={'class': 'form-check',
                                                                                           'placeholder': '=<1'}))
