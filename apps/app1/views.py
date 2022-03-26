from re import template                                     #импорт template отвечающий за внешний вид нашего приложения
from django.db.models import QuerySet                       #импорт queryset для перебора обьектов
from django.core.handlers.wsgi import WSGIRequest           #для просмотра параметров запроса функции
from django.http import HttpResponse                        #для формирования ответа по запросу и обратно к клиенту
# from django.contrib.auth.models import User
from django.shortcuts import render                         #для обработки шаблонов и выдача их в формате HTTP

from apps.auths import views                                #импорт представления аутентификации

from .models import (                                       #импорт моделей
    Account,
    Homework, 
    Student,
)

from django.views import View                               #импорт обработчика запросов 
from django.template import loader                          #для загрузки шаблонов
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
# from django.views.generic.base import TemplateView

from auths.models import CustomUser                         #пользовательская модель
from apps.auths.forms import CustomUserForm                 #пользовательские формы
from auths.forms import CustomUserForm

from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)


class IndexView(View):                                      #Класс представление нашей главной страницы

    template_name = 'login.html'                            #путь до шаблона который будет использован представлении при авторизации пользователя
    queryset = Homework.objects.get_not_deleted()           #список обьектов заданной модели
    
    def get(                                                #функция возращающая значение
        self,                                               #первый параметр метода
        request: WSGIRequest,                               #запрос просмотра
        *args: tuple,                                       #распаковка аргументов 
        **kwargs                                            #распаковка словаря
    )-> HttpResponse:
        
        if not request.user.is_authenticated:               #условие для опознование пользователей
            return render(
                request,
                'login.html'
            )
        homeworks: QuerySet = Homework.objects.filter(      #фильтр обьектов заданной модели
            user=request.user                               #переменная запрашивает данные пользователя
        )
        context:dict = {                                    #словарь добавлен в экземпляр контекста
            'ctx_title': 'Главная страница',
            'ctx_users':homeworks,
        }
        template_name = loader.get_template(                #принимает список шаблонов и возращает первый
            'main.html'
        )
        return HttpResponse(                                #возрат строки
            template_name.render(
                context, request
            ),
            content_type='text/html'
        )

    # def get_html_response(
    #     self,
    #     request:WSGIRequest,
    #     *args:tuple,
    #     **kwargs
    # )
        

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
        template_name='show.html',
        context=context
    )


def logout(request: WSGIRequest) -> HttpResponse:

    dj_logout(request)

    form: CustomUserForm = CustomUserForm(
        request.POST
    )
    context: dict = {
        'form': form,
    }
    return render(
        request,
        'login.html',
        context
    )


def delete():
    pass

class LoginView(View, PermissionsMixin):
    
    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
    )-> HttpResponse:
        
        if not request.user.is_authenticated:
            return render(
                request,
                'login.html'
            )
        homeworks: QuerySet = Homework.objects.filter(
            user=request.user
        )
        context:dict = {
            'ctx_title': 'Главная страница',
            'ctx_users':homeworks,
        }
        template_name = loader.get_template(
            'login.html'
        )
        return HttpResponse(
            template_name.render(
                context, request
            ),
            content_type='text/html'
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
    )  -> HttpResponse:

        if request.method == 'POST':
            email: str = request.POST['email']
            password: str = request.POST['password']

            user: CustomUser = dj_authenticate(
                email=email,
                password=password
            )

            if not user:
                return render(
                    request,
                    'login.html',
                    {'error_message': 'Невереные данные'}
                )
                
            if not user.is_active:
                return render(
                    request,
                    'login.html',
                    {'error_message': 'Ваш аккаунт был удален'}
                )
            dj_login(request, user)

            homeworks: QuerySet = Homework.objects.filter(
            user=request.user
            )
            return render(
                request,
                'main.html',
                {'homeworks': homeworks}
            )
        return render(
            request,
            'login.html'
        )


def register(request: WSGIRequest) -> HttpResponse:

    form: CustomUserForm = CustomUserForm(
        request.POST
    )
    if form.is_valid():
        user: CustomUser = form.save(
            commit=False
        )
        email: str = form.cleaned_data['email']
        password: str = form.cleaned_data['password']
        user.email = email
        user.set_password(password)
        user.save()

        user: CustomUser = dj_authenticate(
            email=email,
            password=password
        )
        if user and user.is_active:

            dj_login(request, user)

            homeworks: QuerySet = Homework.objects.filter(
                user=request.user
            )
            return render(
                request,
                'index.html',
                {'homeworks': homeworks}
            )
    context: dict = {
        'form': form
    }
    return render(
        request,
        'register.html',
        context
    )
