from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import index, index_2

urlpatterns = [
    path('',index),
    path('Стартовая',index_2),
]