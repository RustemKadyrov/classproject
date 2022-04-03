# from unicodedata import name
# from django.contrib import admin
from os import stat
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import (
    CreateHomeWorkView,
    IndexView,
    RegisterView,
    ShowView,
    LoginView,
    LogoutView,
    HomeworkCreateView,
    HomeworkFilesCreateView,
)

urlpatterns = [
    path('',                    IndexView.as_view(),                    name='page_main'),
    path('show/<int:user_id>/', ShowView.as_view,                       name='page_show'),
    path('delete/',             views.delete,                           name='page_delete'),
    path('register/',           RegisterView.as_view(),                 name='page_register'),
    path('login/',              LoginView.as_view(),                    name='page_login'),
    path('logout/',             LogoutView.as_view(),                   name='page_logout'),
    path('create/',             HomeworkCreateView.as_view(),           name='page_create_hw'),
    path('FilesCreate/',        HomeworkFilesCreateView.as_view(),      name='page_create_hw_files.html')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 



