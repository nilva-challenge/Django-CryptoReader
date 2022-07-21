from django.contrib import admin
from .models import ActiveTrackingUser, Order

# Register your models here.
admin.site.register(Order)
admin.site.register(ActiveTrackingUser)