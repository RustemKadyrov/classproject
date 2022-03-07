from django.db.models import QuerySet
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
# from django.contrib.auth.models import User
from django.shortcuts import render

from .models import (
    Account, 
    Student,
)
from auths.models import CustomUser


def index(request: WSGIRequest) -> HttpResponse:
    users:QuerySet = CustomUser.objects.all()
    context:dict = {
        'ctx_title': 'Главная страница',
        'ctx_users':users,
    }
    return render(
        request,
        template_name='university/index.html',
        context=context
    )

def index_2(request: WSGIRequest) -> HttpResponse:
    return HttpResponse(
        '<h1>Страница: Стартовая</h1>',
    )


def index_3(request: WSGIRequest) -> HttpResponse:
    users: QuerySet = CustomUser.objects.all()
    context: dict = {
        'ctx_title': 'Главная страница',
        'ctx_users': users 
   
    }
    return render(
        request,
        'index.html',
        context
    )

def admin_page(request: WSGIRequest) -> HttpResponse:
    users: QuerySet = CustomUser.objects.all()
    context: dict = {
        'ctx_title': 'Страница администратора',
        'users': users 
   
    }
    return render(
        request,
        'admin_page.html',
        context
    )


def show(request: WSGIRequest, pk:int) -> HttpResponse:
    user: CustomUser = CustomUser.objects.get(
        id=pk
    )
    context: dict = {
        'ctx_title': 'Профиль пользователя',
        'ctx_user': user,
   
    }
    return render(
        request,
        template_name='app1/show.html',
        context=context
    )
