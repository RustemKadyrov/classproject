from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from .views import index, index_2, index_3, admin_page, show

urlpatterns = [
    path('',index),
    path('main/',index_2),
    path('second/',index_3),
    path('admin/',admin_page),
    path('show/',show),
    path('__debug__/', include('debug_toolbar.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
