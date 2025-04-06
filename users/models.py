from django.contrib.auth.models import AbstractUser
from django.db import models


class RassvetUser(AbstractUser):
    email = models.EmailField('email address', unique=True, blank=False)
    REQUIRED_FIELDS = ['email']


class ProxyUser(RassvetUser):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
