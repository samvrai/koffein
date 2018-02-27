from django.urls import path

from . import views

app_name = 'coffees'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('coffees/', views.CoffeesView.as_view(), name='coffees'),
    path('batch/', views.BatchView.as_view(), name='batch'),
    path('new_batch/', views.BatchCreate.as_view(), name='new_batch'),
    path('order/', views.UserView.as_view(), name='order'),
    path('update_user/', views.UpdateUserView.as_view(), name='update'),
]
