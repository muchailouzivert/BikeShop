from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    

class Bike(models.Model):
    BIKE_TYPE_CHOICES = [
        ('regular', 'Regular Bike'),
        ('electric', 'Electric Bike'),
    ]
    type = models.CharField(max_length=10, choices=BIKE_TYPE_CHOICES)
    color = models.CharField(max_length=50)
    battery_capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.color}"


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} for {self.bike}"