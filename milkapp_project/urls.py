from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django default admin site (not used in your custom app, but okay to keep)
    path('admin/', admin.site.urls),

    # All app-level routes (home, login, dashboards, etc.)
    path('', include('dairyapp.urls')),
]
