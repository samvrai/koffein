from django.db import models


# Create your models here.
class Order(models.Model):
    closed = models.BooleanField(default=False)
    date = models.DateField()
    shipping = models.FloatField()

    def __str__(self):
        return str(self.date)


class User(models.Model):
    orders = models.ManyToManyField(Order)
    name = models.CharField(max_length=200)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Coffee(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    intensity = models.IntegerField()
    users = models.ManyToManyField(User, through='CoffeeUser')

    def __str__(self):
        return self.name


class CoffeeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
