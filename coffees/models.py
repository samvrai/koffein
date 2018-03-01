from django.db import models


# Create your models here.
class Coffee(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    intensity = models.IntegerField()

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    closed = models.BooleanField(default=False)
    date = models.DateField()
    shipping = models.FloatField()

    def __str__(self):
        return str(self.date)


class CoffeeUser(models.Model):
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class CoffeeUserOrder(models.Model):
    coffee_user = models.ForeignKey(CoffeeUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.coffee_user.name
