from re import template                                     #импорт template отвечающий за внешний вид нашего приложения
from typing import Optional                                 #анотация неопределнного 
from django.db.models import QuerySet                       #импорт queryset для перебора обьектов
from django.core.handlers.wsgi import WSGIRequest           #для просмотра параметров запроса функции
from django.http import HttpResponse                        #для формирования ответа по запросу и обратно к клиенту
# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render                         #для обработки шаблонов и выдача их в формате HTTP
from django.views import View                               #импорт обработчика запросов 
from django.template import loader                          #для загрузки шаблонов
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)

from apps.auths import views                                #импорт представления аутентификации

from .models import (                                       #импорт моделей
    Account,
    Homework, 
    Student,
    Professor
)

# from django.views.generic.base import TemplateView
from apps.app1.forms import HomeworkForm, FileForm
from auths.models import CustomUser                         #пользовательская модель
from apps.auths.forms import CustomUserForm                 #пользовательские формы
from auths.forms import CustomUserForm
from abstract.handlers import ViewHandler

class IndexView(ViewHandler, View):                                      #Класс представление нашей главной страницы

    queryset: QuerySet=Homework.objects.get_not_deleted()
    template_name: str='index.html'                            #путь до шаблона который будет использован представлении при авторизации пользователя
        
    def get(                                                #функция возращающая значение
        self,                                               #первый параметр метода
        request: WSGIRequest,                               #запрос просмотра
        *args: tuple,                                       #распаковка аргументов 
        **kwargs:dict,                                           #распаковка словаря
    )-> HttpResponse:
        
        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response
            
        homeworks: QuerySet = self.queryset.filter(
            user=request.user,
        )
        query:str = request.GET.get('q')
        if query:
            homeworks=homeworks.filter(
                Q(title__icontains=query) |
                Q(subject__icontains=query)
            ).distinct()
        
        if not homeworks:
            homeworks = self.queryset
    
        return self.get_http_response(
            request,
            template_name=self.template_name,
            context={
                'ctx_title': 'Главная страница',
                'ctx_homework':homeworks,
                'ctx_users': request.user,
            }
        )

class HomeworkDetailsView(ViewHandler, View):

    queryset: QuerySet = Homework.objects.get_not_deleted()

    template_name: str ='homework_detail.html'    

    def get(
        self,
        request: WSGIRequest,
        homework_id: int, 
        *args: tuple,
        **kwargs: dict
        ) -> HttpResponse:
        
        homework = self.queryset.filter(user=self.request.user)\
                .get(id=homework_id)

        context: dict = {
            'homework': homework
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )       

class AdminView(ViewHandler, View):
    
    template_name: str = 'admin_page.html'
    
    def get(self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict,
        ) -> HttpResponse:

        users: QuerySet = CustomUser.objects.filter(
            is_active=True
        )
        context: dict = {
            'ctx_title': 'Главная страница',
            'ctx_users': users,
            }

        
        
        return self.get_http_response(
            request,
            self.template_name,
            context
        )  

class ShowView(ViewHandler, View):

    QuerySet: QuerySet = Homework.objects.get_not_deleted()

    template_name = 'show.html'
    
    def get(
        self,
        request: WSGIRequest,
        *args:tuple,
        **kwargs:dict
    ):
        homework_id: int = kwargs.get('homework_id',0)
        homework: Optional[Homework] = None

        try:
            homework = self.queryset.filter(user=self.request.user)\
                .get(id=homework_id)

        except Homework.DoesNotExist:
            return self.get_http_response(
                request,
                'login.html'
            )
        else:
            context:dict = {
                'ctx_title': 'Профиль',
                'ctx_homework': homework,
            }

            return self.get_http_response(
                request,
                self.template_name,
                context,
            )

class LogoutView(ViewHandler, View):

    def get(self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
        ) -> HttpResponse:

        dj_logout(request)

        form: CustomUserForm = CustomUserForm(
            request.POST
            )
        context: dict = {
            'form': form,
            }
  
        template_name: str = 'login.html'

        return self.get_http_response(
            request,
            template_name,
            context
        )

class DeleteView(ViewHandler, View):
    
    template_name: str = 'admin_page.html'

    def get(self,
        request: WSGIRequest,
        user_id: int,
        *args: tuple,
        **kwargs: dict,
        ) -> HttpResponse:

        user = CustomUser.objects.get(id=user_id)
        print(user)
        user.delete()
        

        context: dict = {
            'ctx_title': 'Главная страница',
            'ctx_users': CustomUser.objects.all(),
            }
            
        return self.get_http_response(
            request,
            self.template_name,
            context
        )  

class LoginView(ViewHandler, View):

    def get(self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
        ) -> HttpResponse:

        form: CustomUserForm = CustomUserForm(
            request.POST
            )
        context: dict = {
            'form': form
        }        
        
        template_name: str = 'login.html'
        
        return self.get_http_response(
            request,
            template_name,
            context
        )

    def post(self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
        ) -> HttpResponse:
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
        context: dict = {
            'homeworks': homeworks
        }
       
        template_name: str = 'main.html'
        
        return self.get_http_response(
            request,
            template_name,
            context
        )
    
class RegisterView(ViewHandler, View):

    ftemplate_name = 'homework.html'      
    queryset = Homework.objects.get_not_deleted()           
    
    def get(                                                
        self,                                               
        request: WSGIRequest,                                                                         
    )-> HttpResponse:
        
        form: CustomUserForm = CustomUserForm(
            request.POST                               
        )
        context:dict = {                                    
            'form': form
        }
        template_name = 'register.html'

        return self.get_http_response(
            request,
            template_name,
            context
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs
    )  -> HttpResponse:

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
                context: dict = {
                    'homeworks':homeworks
                }
                template_name: str = 'main.html'
                
                return self.get_http_response(
                    request,
                    template_name,
                    context
                )

class HomeworkCreateView(ViewHandler, View):

    form: HomeworkForm = HomeworkForm
    template_name: str = 'homework_create.html'

    def get(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:

        response: Optional[HttpResponse] = \
            self.get_validated_response(
                request
            )
        if response:
            return response

        context: dict = {
            'ctx_form': self.form(),
        }
        return self.get_http_response(
            request,
            self.template_name,
            context
        )

    def post(
        self,
        request: WSGIRequest,
        *args: tuple,
        **kwargs: dict
    ) -> HttpResponse:

        _form: HomeworkForm = self.form(
            request.POST or None,
            request.FILES or None
        )
        if not _form.is_valid():
            context: dict = {
                'ctx_form': _form,
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework: Homework = _form.save(
            commit=False
        )
        homework.user = request.user
        homework.logo = request.FILES['logo']

        file_type: str = homework.logo.url.split('.')[-1].lower()

        if file_type not in Homework.IMAGE_TYPES:

            context: dict = {
                'ctx_form': _form,
                'ctx_homework': homework,
                'error_message': 'PNG, JPG, JPEG',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        homework.save()

        context: dict = {
            'homework': homework
        }
        return self.get_http_response(
            request,
            'homework_detail.html',
            context
        )

class HomeworkFilesCreateView(ViewHandler, View):

    queryset: QuerySet = Homework.objects.get_not_deleted()
    form: FileForm = FileForm
    template_name:str = 'homework_files_create.html'

    def post(
        self,
        request:WSGIRequest,
        homework_id:int,
        *args:tuple,
        **kwargs:dict
    ) -> HttpResponse:

        _form:FileForm = self.form(
            request.POST or None,
            request.FILES or None
        )
        homework: Homework = get_object_or_404(
            Homework,
            id=homework_id
        )
        if not form.is_valid():
            context:dict = {
                'ctx_form':_form,
                'ctx_homework':homework,
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        files = homework.files.get_not_deleted()
        form_title: str = _form.cleaned_data_get('title')

        file:File
        for file in files:
            if file.title != form_title:
                continue

            context: dict = {
                'ctx_homework':homework,
                'ctx_form':_form,
                'error_message': 'Файл уже добавлен',
            }
            return self.get_http_response(
                request,
                self.template_name,
                context
            )
        file:File = form.save(
            commit=False
        )
        file.homework = homework
        file.obj = request.FILES['obj']