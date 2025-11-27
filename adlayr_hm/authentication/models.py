from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):

    ADMIN = 'Admin', 'admin'
    USER = 'User', 'user'
    VENDOR = 'Vendor', 'Vendor'

class Profile(AbstractUser):

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=RoleChoices.choices)
    phone_num = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'profile'

        verbose_name_plural = 'profiles'

    def __str__(self):

        return f'{self.username}' 