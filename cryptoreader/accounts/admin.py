from django.contrib import admin
from .models import KucoinAccount, User

# Register your models here.
class KucoinAccountModelAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "type",
        "currency",
        "balance",
        "available",
        "holds",
    ]


admin.site.register(KucoinAccount, KucoinAccountModelAdmin)
admin.site.register(User)
