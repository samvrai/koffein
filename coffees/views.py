from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.shortcuts import redirect
from django.views import generic
from .models import Coffee, Order, User, CoffeeUserOrder, CoffeeUserOrderQuantity
from coffees.forms import OrderCreateForm, OrderUpdateForm, UserCreateForm, UserUpdateForm, CoffeeSelectorForm


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
        return User.objects.filter(coffeeuserorder__order=order)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderUserListView, self).get_context_data(**kwargs)
        context['order'] = self.kwargs['pk']
        context['closed'] = Order.objects.get(pk=self.kwargs['pk']).closed
        return context


class OrderDetailsView(generic.TemplateView):
    template_name = 'coffees/order_details.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailsView, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        try:
            cuo = CoffeeUserOrder.objects.filter(order=order)
            coffees = CoffeeUserOrderQuantity.objects.filter(
                cuo__in=cuo).values('coffee_id', 'coffee__name', 'coffee__price').annotate(
                quantity=Sum('quantity')).annotate(total=ExpressionWrapper(F('coffee__price') *
                                                                           F('quantity'), output_field=FloatField()))
            context['coffees'] = coffees
            total = 0
            for coffee in coffees:
                total += coffee['total']
            total += order.shipping
            context['shipping'] = order.shipping
            context['total'] = total
        except Exception as ex:
            return context

        return context


class OrderCreate(generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = '/orders'


class OrderUpdate(generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = '/orders'


class OrderDelete(generic.DeleteView):
    model = Order
    success_url = '/orders'


class UserListView(generic.ListView):
    model = User

    def get_queryset(self):
        try:
            username = self.request.GET['username']
        except KeyError:
            username = ''

        if username != '':
            object_list = self.model.objects.filter(name__contains=username)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class UserOrderListView(generic.TemplateView):
    template_name = 'coffees/coffeeuserorder_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserOrderListView, self).get_context_data(**kwargs)
        user = kwargs['pk']
        try:
            cuo = CoffeeUserOrder.objects.filter(user=user).values('order__date', 'paid', 'order_id')

        except Exception as ex:
            return context

        context['orders'] = cuo
        context['user'] = user
        return context


class UserCreate(generic.FormView):
    template_name = 'coffees/user_form.html'
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['order'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return str(self.kwargs['pk']) + '/coffees'

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(name=request.POST['name'])
        except User.DoesNotExist:
            user = User(name=request.POST['name'])
            user.save()
        order = Order.objects.get(id=int(request.POST['orders']))
        try:
            CoffeeUserOrder.objects.get(order=order, user=user)
        except CoffeeUserOrder.DoesNotExist:
            cuo = CoffeeUserOrder(order=order, user=user)
            cuo.save()
        return redirect('/update_user/' + str(order.id) + '/' + str(user.id))


class CoffeeSelector(generic.FormView):
    template_name = 'coffees/coffee_selector.html'
    form_class = CoffeeSelectorForm

    def get_form_kwargs(self):
        kwargs = super(CoffeeSelector, self).get_form_kwargs()
        kwargs['user'] = self.kwargs['user']
        kwargs['order'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CoffeeSelector, self).get_context_data(**kwargs)
        context['user'] = self.kwargs['user']
        context['order'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        selected = []
        for i in request.POST:
            if i.startswith('coffee'):
                selected.append(int(i.split('_')[1]))

        order = kwargs['pk']
        user = kwargs['user']
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user)
        except CoffeeUserOrder.DoesNotExist:
            return None

        for coffee in selected:
            coffee_aux = Coffee.objects.get(pk=coffee)
            if coffee_aux not in cuo.coffees.all():
                cuoq = CoffeeUserOrderQuantity(coffee=coffee_aux, cuo=cuo)
                cuoq.save()

        coffees_remove = cuo.coffees.exclude(id__in=selected)

        for coffee in coffees_remove:
            cuo.coffees.remove(coffee)

        return redirect('/update_user/' + str(self.kwargs['pk']) + '/' + str(self.kwargs['user']) + '/checkout')


class UserUpdate(generic.FormView):
    template_name = 'coffees/update_user.html'
    form_class = UserUpdateForm

    def get_form_kwargs(self):
        kwargs = super(UserUpdate, self).get_form_kwargs()
        kwargs['user'] = self.kwargs['user']
        kwargs['order'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['user'] = self.kwargs['user']
        context['order'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        order = kwargs['pk']
        user = kwargs['user']
        coffees = []
        for data in request.POST:
            if data.startswith('coffee'):
                coffees.append({'key': int(data.split('_')[1]),  'quantity': int(request.POST[data])})
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user)
        except CoffeeUserOrder.DoesNotExist:
            return None

        for coffee in coffees:
            c_2 = CoffeeUserOrderQuantity.objects.get(coffee=coffee['key'], cuo=cuo)
            c_2.quantity = coffee['quantity']
            c_2.save()
        return redirect('/order/' + str(order))


class UserDelete(generic.DeleteView):
    model = CoffeeUserOrder

    def get_success_url(self):
        return '/order/' + str(self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        order = kwargs['pk']
        user = kwargs['user']
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user)
        except CoffeeUserOrder.DoesNotExist:
            return None
        cuo.delete()
        return redirect(self.get_success_url())


class UserOrderDetailsView(generic.TemplateView):
    template_name = 'coffees/user_details.html'

    def get_context_data(self, **kwargs):
        context = super(UserOrderDetailsView, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        user = self.kwargs['user']
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user)
            coffees = CoffeeUserOrderQuantity.objects.filter(
                cuo=cuo).values('coffee_id', 'coffee__name', 'coffee__price').annotate(
                quantity=Sum('quantity')).annotate(total=ExpressionWrapper(F('coffee__price') *
                                                                           F('quantity'), output_field=FloatField()))
            context['coffees'] = coffees
            users = CoffeeUserOrder.objects.filter(order=order).count()
            total = 0
            for coffee in coffees:
                total += coffee['total']
            total += order.shipping / users
            context['shipping'] = order.shipping / users
            context['total'] = total
            context['order'] = self.kwargs['pk']
            context['closed'] = order.closed
        except Exception as ex:
            return context

        return context


