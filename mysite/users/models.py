from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    class Role(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        SHOP_OWNER = 'shop_owner', 'Shop Owner'
        CUSTOMER = 'customer', 'Customer'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
