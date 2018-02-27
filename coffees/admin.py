from django.contrib import admin

from .models import Coffee, Order

admin.site.register(Coffee)
admin.site.register(Order)