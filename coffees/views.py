from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.shortcuts import redirect
from django.views import generic
from django.core import mail
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Coffee, Order, User, CoffeeUserOrder, CoffeeUserOrderQuantity
from coffees.forms import OrderCreateForm, OrderUpdateForm, UserCreateForm, UserUpdateForm, CoffeeSelectorForm


# Create your views here.
class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'base.html'
    login_url = '/login/'
    redirect_field_name = ''


class CoffeeListView(LoginRequiredMixin, generic.ListView):
    model = Coffee
    context_object_name = 'coffee_list'
    login_url = '/login/'


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    context_object_name = 'order_list'
    login_url = '/login/'


class OrderUserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'coffees/order_user.html'
    context_object_name = 'user_list'
    login_url = '/login/'

    def get_queryset(self):
        order = self.kwargs['pk']
        return User.objects.filter(coffeeuserorder__order=order)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderUserListView, self).get_context_data(**kwargs)
        context['order'] = self.kwargs['pk']
        context['closed'] = Order.objects.get(pk=self.kwargs['pk']).closed
        return context


class OrderDetailsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'coffees/order_details.html'
    login_url = '/login/'

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


class OrderCreate(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = '/orders'
    login_url = '/login/'


class OrderUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = '/orders'
    login_url = '/login/'


class OrderDelete(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = '/orders'
    login_url = '/login/'


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'coffees/user_list.html'

    def get_queryset(self):
        try:
            username = self.request.GET['username']
        except KeyError:
            username = ''

        if username != '':
            object_list = self.model.objects.filter(username__contains=username)
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class UserOrderListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'coffees/coffeeuserorder_list.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(UserOrderListView, self).get_context_data(**kwargs)
        user_target = kwargs['pk']
        try:
            cuo = CoffeeUserOrder.objects.filter(user=user_target).values('order__date', 'paid', 'order_id')

        except Exception as ex:
            return context

        context['orders'] = cuo
        context['user_target'] = user_target
        return context


class UserCreate(LoginRequiredMixin, generic.FormView):
    template_name = 'coffees/user_form.html'
    form_class = UserCreateForm
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserCreate, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if 'pk' in self.kwargs:
            context['order'] = self.kwargs['pk']
        return context

    def get_success_url(self):
        return str(self.kwargs['pk']) + '/coffees'

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.POST['username'])
        except User.DoesNotExist:
            pw = User.objects.make_random_password()
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['username'] + '@versia.com',
                                            password=pw)
            user.save()
            mail.send_mail('Koffein Service', 'Tu contraseña es ' + pw, 'asier.esteban@versia.com',
                           [request.POST['username'] + '@versia.com'])
        except Exception as ex:
            tr = ex

        if 'orders' in request.POST and request.POST['orders'] != '':
            order = Order.objects.get(id=int(request.POST['orders']))
        else:
            return redirect('/users/')
        try:
            CoffeeUserOrder.objects.get(order=order, user=user)
        except CoffeeUserOrder.DoesNotExist:
            cuo = CoffeeUserOrder(order=order, user=user)
            cuo.save()
        return redirect('/update_user/' + str(order.id) + '/' + str(user.id))


class CoffeeSelector(LoginRequiredMixin, generic.FormView):
    template_name = 'coffees/coffee_selector.html'
    form_class = CoffeeSelectorForm
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super(CoffeeSelector, self).get_form_kwargs()
        kwargs['user_target'] = self.kwargs['user_target']
        kwargs['order'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CoffeeSelector, self).get_context_data(**kwargs)
        context['user_target'] = self.kwargs['user_target']
        context['order'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        selected = []
        for i in request.POST:
            if i.startswith('coffee'):
                selected.append(int(i.split('_')[1]))

        order = Order.objects.get(id=kwargs['pk'])
        user_target = User.objects.get(id=kwargs['user_target'])
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user_target)
        except CoffeeUserOrder.DoesNotExist:
            cuo = CoffeeUserOrder(order=order, user=user_target)

        for coffee in selected:
            coffee_aux = Coffee.objects.get(pk=coffee)
            if coffee_aux not in cuo.coffees.all():
                cuoq = CoffeeUserOrderQuantity(coffee=coffee_aux, cuo=cuo)
                cuoq.save()

        coffees_remove = cuo.coffees.exclude(id__in=selected)

        for coffee in coffees_remove:
            c = CoffeeUserOrderQuantity.objects.get(coffee=coffee, cuo=cuo)
            c.delete()

        return redirect('/update_user/' + str(self.kwargs['pk']) + '/' + str(self.kwargs['user_target']) + '/checkout')


class UserUpdate(LoginRequiredMixin, generic.FormView):
    template_name = 'coffees/update_user.html'
    form_class = UserUpdateForm
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super(UserUpdate, self).get_form_kwargs()
        kwargs['user_target'] = self.kwargs['user_target']
        kwargs['order'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['user_target'] = self.kwargs['user_target']
        context['order'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        order = kwargs['pk']
        user_target = kwargs['user_target']
        coffees = []
        for data in request.POST:
            if data.startswith('coffee'):
                coffees.append({'key': int(data.split('_')[1]),  'quantity': int(request.POST[data])})
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user_target)
        except CoffeeUserOrder.DoesNotExist:
            return None

        if len(coffees) == 0:
            cuo.delete()
        else:
            for coffee in coffees:
                c_2 = CoffeeUserOrderQuantity.objects.get(coffee=coffee['key'], cuo=cuo)
                c_2.quantity = coffee['quantity']
                c_2.save()

        if request.user.is_staff:
            returner = '/order/' + str(order)
        else:
            returner = '/orders'
        return redirect(returner)


class UserDelete(LoginRequiredMixin, generic.DeleteView):
    model = CoffeeUserOrder
    login_url = '/login/'

    def get_success_url(self):
        return '/order/' + str(self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        order = kwargs['pk']
        user_target = kwargs['user_target']
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user_target)
        except CoffeeUserOrder.DoesNotExist:
            return None
        cuo.delete()
        return redirect(self.get_success_url())


class UserOrderDetailsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'coffees/user_details.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(UserOrderDetailsView, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        user_target = self.kwargs['user_target']
        try:
            cuo = CoffeeUserOrder.objects.get(order=order, user=user_target)
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

