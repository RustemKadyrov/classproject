from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from .views import index, index_2, index_3

urlpatterns = [
    path('',index),
    path('in/',index_2),
    path('dop/',index_3),
]