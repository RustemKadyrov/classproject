from django.utils import timezone
from datetime import datetime
import email
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    
    def create_user(
        self,
        email: str,
        password: str, 
        **kwargs: dict
    ) -> 'CustomUser':
        
        if not email:
            raise ValidationError('Email required')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **kwargs: dict
    ) -> 'CustomUser':

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        'Почта/Логин',unique=True
    )
    is_active = models.BooleanField(default=True)
    datetime_joined = models.DateTimeField(default=timezone.now)
    is_root = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    datetime_joined = models.DateTimeField(
        verbose_name='Время регистрации',
        auto_now=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = (
            'email',
        )
        verbose_name = 'Почта/Логин'
        verbose_name_plural = 'Почты/Логины'

    # def save(self,*args,**kwargs) ->None:
    #     if(self.email != self.email.lower()):
    #         raise ValidationError (
    #             'Ваш email "%(email)%" должен быть в написан маленькими буквами',
    #             code = 'lower.case.email_error',
    #             params= ('email': self.email)
    #     super().save(*args,**kwargs)