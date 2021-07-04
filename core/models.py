from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    designation = models.CharField(max_length=30)

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.designation)


class Restaurant(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    votes = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
