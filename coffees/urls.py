from django.urls import path

from . import views

app_name = 'coffees'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coffees/', views.CoffeeListView.as_view(), name='coffees'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderUserListView.as_view(), name='order_list'),
    path('new_order/', views.OrderCreate.as_view(), name='new_order'),
    path('update_order/<int:pk>', views.OrderUpdate.as_view(), name='update_order'),
    path('delete_order/<int:pk>', views.OrderDelete.as_view(), name='delete_order'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserOrderListView.as_view(), name='user_orders'),
    path('new_user/<int:order>', views.UserCreate.as_view(), name='new_user'),
    path('update_user/<int:order>', views.UserUpdate.as_view(), name='update_user'),
]
