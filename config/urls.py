from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # views
    path('', include('backend.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),

    # rest-api
    path('api/', include('api.urls')),
]
