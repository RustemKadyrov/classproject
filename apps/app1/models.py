from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Account(models.Model):

    ACCOUNT_FULL_NAME_MAX_LENGTH = 20

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    full_name = models.CharField(
        max_length=ACCOUNT_FULL_NAME_MAX_LENGTH
    )
    description = models.TextField()

    def __str__(self) -> str:
        return f'Аккаунт: {self.user.id} / {self.full_name}'

    class Meta:
        ordering = (
            'full_name',
        )
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

class Group(models.Model):

    GROUP_NAME_MAX_LENGTH = 10

    name = models.CharField(
        max_length = GROUP_NAME_MAX_LENGTH,
    )

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

class Student(models.Model):
    MAX_AGE = 27

    account = models.OneToOneField(
        Account,
        verbose_name = 'Аккаунт',
        on_delete = models.CASCADE
    )
    age = models.IntegerField(
        verbose_name = 'возраст студента',
    )
    group = models.ForeignKey(
        Group,
        verbose_name = 'группа',
        on_delete = models.PROTECT
    )
    GPA = models.FloatField(
       verbose_name = 'Среднее значение GPA',
    )

    def __str__ (self) -> str:
        return 'Студент: {0} / {1} / {2}' . format(
            self.account.full_name,
            self.age,
            self.gpa,
        )

    def safe(
        self,
        *args:tuple,
        **kwargs: dict
    ) -> None:
        if self.age > self.MAX_AGE:
            # self.age = self.MAX_AGE
            raise ValidationError (
                'Допустимый возраст: {self.MAX_AGE}'
            )
        super().save(*args, **kwargs)

    class Meta:
        ordering = (
            'GPA',
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
