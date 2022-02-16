from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import Account, Student


def index(request: WSGIRequest) -> HttpResponse:
    student: Student = Student.objects.first()
    account: Account = student.account
    user: User = account.user

    text: str = f'''<h1>Имя: {user.first_name} <br>
                        Аккаунт: {account.full_name} <br>
                        GPA Студента: {student.gpa}
    </h1>'''


    response: HttpResponse = HttpResponse(text)
    return response

def index_2(request: WSGIRequest) -> HttpResponse:
    return HttpResponse(
        '<h1>Страница: Стартовая</h1>'
    )

