from signal import setitimer
from xml.dom.minidom import Document
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path(settings.ADMIN_SITE_URL, admin.site.urls),
    path('', include('app1.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/',include('debug_toolbar.urls')),]    
