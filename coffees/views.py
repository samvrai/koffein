from django.shortcuts import render, redirect
from django.views import generic
from .models import Coffee, CoffeeUser, Order, User
from coffees.forms import SearchForm, OrderCreate, OrderUpdate


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'coffees/menu.html'


class CoffeesView(generic.ListView):
    template_name = 'coffees/coffees.html'
    context_object_name = 'coffee_list'

    def get_queryset(self):
        return Coffee.objects.all()


class OrderView(generic.ListView):
    template_name = 'coffees/orders.html'
    context_object_name = 'order_list'

    def get_queryset(self):
        return Order.objects.all()


class OrderCreate(generic.CreateView):
    model = Order
    form_class = OrderCreate
    success_url = '/order'


class OrderUpdate(generic.UpdateView):
    model = Order
    form_class = OrderUpdate
    success_url = '/order'


class OrderDelete(generic.DeleteView):
    model = Order
    success_url = '/order'


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
            coffee_list = CoffeeUser.objects.defer('coffee', 'quantity').filter(user=user.id, cofeeuserorder__id=order.id)
            return redirect('/update_user/', coffee_list)

    def get(self, request, *args, **kwargs):
        form = SearchForm()
        return render(request, self.template_name, {'form': form})


class UpdateUserView(generic.FormView):
    template_name = 'coffees/update_user.html'
    form_class = None
    success_url = '/order/'

    def form_valid(self, form):
        return True
