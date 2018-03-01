from django.urls import path

from . import views

app_name = 'coffees'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coffees/', views.CoffeesView.as_view(), name='coffees'),
    path('order/', views.OrderView.as_view(), name='order'),
    path('new_batch/', views.OrderCreate.as_view(), name='new_order'),
    path('update_batch/<int:pk>', views.OrderUpdate.as_view(), name='update_order'),
    path('delete_batch/<int:pk>', views.OrderDelete.as_view(), name='delete_order'),
    path('user/', views.UserView.as_view(), name='user'),
    path('update_user/', views.UpdateUserView.as_view(), name='update_user'),
]
