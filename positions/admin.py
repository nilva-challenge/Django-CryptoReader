from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'symbol', 'is_active', 'created_at',)
    list_filter = ('is_active',)
    search_fields = ('user', 'symbol',)
