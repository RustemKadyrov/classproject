from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render


def index(request: WSGIRequest) -> HttpResponse:
    user: User = User.objects.first()
    name: str = user.first_name
    text: str = f'<h1>Имя: {name}</h1>'

    response: HttpResponse = HttpResponse(text)
    return response

