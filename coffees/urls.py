from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'coffees'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coffees/', views.CoffeeListView.as_view(), name='coffees'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('order/<int:pk>', views.OrderUserListView.as_view(), name='order_list'),
    path('order/<int:pk>/details', views.OrderDetailsView.as_view(), name='order_details'),
    path('new_order/', views.OrderCreate.as_view(), name='new_order'),
    path('update_order/<int:pk>', views.OrderUpdate.as_view(), name='update_order'),
    path('delete_order/<int:pk>', views.OrderDelete.as_view(), name='delete_order'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('user/<int:pk>', views.UserOrderListView.as_view(), name='user_orders'),
    path('user/<int:pk>/<int:user_target>/details', views.UserOrderDetailsView.as_view(), name='user_order_details'),
    path('new_user/<int:pk>', views.UserCreate.as_view(), name='new_user'),
    path('new_user/<int:pk>/coffees', views.UserUpdate.as_view(), name='new_user_coffees'),
    path('update_user/<int:pk>/<int:user_target>', views.CoffeeSelector.as_view(), name='select_coffee'),
    path('update_user/<int:pk>/<int:user_target>/checkout', views.UserUpdate.as_view(), name='update_user'),
    path('delete_user/<int:pk>/<int:user_target>', views.UserDelete.as_view(), name='delete_user'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
]
