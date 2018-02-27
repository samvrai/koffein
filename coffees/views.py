from django.shortcuts import render, redirect
from django.views import generic
from .models import Coffee, CoffeeUser, Order, User
from coffees.forms import SearchForm, UpdateUserForm, OrderForm


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'coffees/menu.html'


class CoffeesView(generic.ListView):
    template_name = 'coffees/coffees.html'
    context_object_name = 'coffee_list'

    def get_queryset(self):
        return Coffee.objects.all()


class BatchView(generic.ListView):
    template_name = 'coffees/orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.all()


class BatchCreate(generic.CreateView):
    model = Order
    form_class = OrderForm


class UserView(generic.TemplateView):
    template_name = 'coffees/user.html'

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(name=form.cleaned_data['username'])
            except User.DoesNotExist:
                user = User(name=form.cleaned_data['username'])
                user.save()
            order = Order.objects.get(closed=False)
            coffee_list = CoffeeUser.objects.defer('coffee', 'quantity').filter(user=user.id, order=order.id)
            return redirect('/update_user/', coffee_list)

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        return render(request, self.template_name, {'form': form})


class UpdateUserView(generic.FormView):
    template_name = 'coffees/update_user.html'
    form_class = UpdateUserForm
    success_url = '/order/'

    def form_valid(self, form):
        return True
