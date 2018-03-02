from django.views import generic
from .models import Coffee, Order, User
from coffees.forms import OrderCreate, OrderUpdate, UserCreate


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'base.html'


class CoffeeListView(generic.ListView):
    model = Coffee
    context_object_name = 'coffee_list'


class OrderListView(generic.ListView):
    model = Order
    context_object_name = 'order_list'


class OrderUserListView(generic.ListView):
    model = User
    template_name = 'coffees/order_user.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        order = self.kwargs['pk']
        return User.objects.filter(orders__id=order)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderUserListView, self).get_context_data(**kwargs)
        context['order'] = self.kwargs['pk']
        return context


class OrderCreate(generic.CreateView):
    model = Order
    form_class = OrderCreate
    success_url = '/orders'


class OrderUpdate(generic.UpdateView):
    model = Order
    form_class = OrderUpdate
    success_url = '/orders'


class OrderDelete(generic.DeleteView):
    model = Order
    success_url = '/order'


class UserListView(generic.ListView):
    model = User

    def get_queryset(self):
        try:
            username = self.request.GET['username']
        except KeyError:
            username = ''

        if username != '':
            object_list = self.model.objects.filter(name__icontains=username)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class UserOrderListView(generic.ListView):
    model = None
    template_name = 'coffees/coffeeuserorder_list.html'


class UserCreate(generic.FormView):
    template_name = 'coffees/user_form.html'
    form_class = UserCreate

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['order'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return str(self.kwargs['pk']) + '/coffees'

    def post(self, request, *args, **kwargs):
        user = User(name=request.POST['name'])
        order = Order.objects.get(id=int(request.POST['orders']))
        user.save()
        user.orders.add(order)


class UserUpdate(generic.FormView):
    template_name = 'coffees/update_user.html'

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)

