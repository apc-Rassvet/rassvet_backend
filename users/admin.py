from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ProxyUser


@admin.register(ProxyUser)
class ProxyUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
