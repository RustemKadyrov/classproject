from django.urls import path
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
    #path('', include('app1.urls')),
]
