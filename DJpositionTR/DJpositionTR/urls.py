from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('useAuthApp.urls')),
    path('api/', include('DjReader.urls')),

]
