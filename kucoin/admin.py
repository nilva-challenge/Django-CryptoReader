from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''
        Register and change Order admin page
    '''

    list_filter = ('isActive',)
    list_display = ('user', 'clientOid', 'isActive')
    list_editable = ('isActive',)
