from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    closed = models.BooleanField(default=False)
    date = models.DateField()
    shipping = models.FloatField()

    def __str__(self):
        return str(self.date)


class Coffee(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    intensity = models.IntegerField()

    def __str__(self):
        return self.name


class CoffeeUserOrder(models.Model):
    paid = models.BooleanField(default=False)
    coffees = models.ManyToManyField(Coffee, through='CoffeeUserOrderQuantity')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('user', 'order')

    def __str__(self):
        return self.user.username


class CoffeeUserOrderQuantity(models.Model):
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    cuo = models.ForeignKey(CoffeeUserOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ('coffee', 'cuo')
