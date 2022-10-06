from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {
             'fields':
             ('name', 'kucoin_key', 'kucoin_secret', 'kucoin_passphrase')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),)

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = ('username', 'name', 'is_staff', 'is_active')
    list_editable = ('is_staff', 'is_active')
