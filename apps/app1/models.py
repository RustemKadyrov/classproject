from datetime import (
    datetime,
)

from django.db import (
    models,
)
# from django.db.models import (
#     QuerySet,
# )
from django.core.exceptions import(
    ValidationError,
)
from django.contrib.auth.models import User

from abstract.models import AbstractDateTime

from django.db.models import (
    QuerySet,
)


class AccountQuerySet(QuerySet):
    
    def get_superusers(self) -> QuerySet:
        return self.filter(
            user__is_superuser=True
        )


class Account(AbstractDateTime):

    ACCOUNT_FULL_NAME_MAX_LENGTH = 20

    user = models.OneToOneField(
        User,
        on_delete = models.CASCADE
    )
    full_name = models.CharField(
        max_length=ACCOUNT_FULL_NAME_MAX_LENGTH
    )
    description = models.TextField()

    objects = AccountQuerySet().as_manager()

    def __str__(self) -> str:
        return f'Account: {self.user.id}  {self.full_name}' 
    

    class Meta:
        ordering = (
            'full_name',
        )
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class GroupQuerySet(QuerySet):

    HIGH_GPA_LEVEL = 4.0

    def get_students_with_high_gpa(self) -> QuerySet:
        return self.filter(
            student__gpa = self.HIGH_GPA_LEVEL
        )



class Group(AbstractDateTime):
    GROUP_NAME_MAX_LENGTH = 10

    name = models.CharField(
        max_length = GROUP_NAME_MAX_LENGTH
    )
    objects = GroupQuerySet().as_manager()
    def __str__(self) -> str:
        return f'Group: {self.name}'

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class StudentQuerySet(QuerySet):
    ADULT_AGE = 18

    def get_adult_student(self) -> QuerySet:
        return self.filter(
            age__gte=self.ADULT_AGE
        )


class Student(AbstractDateTime):
    MAX_AGE = 27
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE
    )
    age = models.IntegerField(
        'Возраст студента', 
    )
    gpa = models.FloatField(
        'Средний бал'
    )
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT
    )
    objects = StudentQuerySet().as_manager()

    def __str__(self) -> str:
        return f'Student: {self.account}, {self.age}, \
            {self.gpa}, {self.group.name}'
    
    def save(self,
        *args: tuple,
        **kwargs: dict
        ) -> None:
        if self.age > self.MAX_AGE:
            self.age = self.MAX_AGE
            raise ValidationError(
                f'Допустимый восраст : {self.MAX_AGE}'
            )
        super().save(*args, **kwargs)
    
    def delete(self) -> None:
        breakpoint()

        datetime_now: datetime = datetime_now()

        self.save(
            update_fields=['datetmie_deleted']
        )
        super().delete()


    class Meta:
        ordering = (
            'account',
            'age',
            'group',
            'gpa'
        )
        verbose_name = 'Студент'
        verbose_name_plural = 'Стундеты'


class Professor(AbstractDateTime):
    FULL_NAME_MAX_LENGTH = 20

    TOPIC_JAVA = 'java'
    TOPIC_PYTHON= 'python'
    TOPIC_TYPECSCRIPT = 'typescript'
    TOPIC_RUBY = 'ruby'
    TOPIC_GOLANG = 'golang'
    TOPIC_SQL= 'sql'
    TOPIC_SWIFT = 'swift'
    TOPIC_PHP = 'php'
    TOPIC_DELPHI = 'delphi'
    TOPIC_PERL = 'perl'

    TOPIC_CHOICES = (
        (TOPIC_JAVA, 'Java'),
        (TOPIC_PYTHON, 'Python'),
        (TOPIC_TYPECSCRIPT, 'TypeScrips'),
        (TOPIC_RUBY,'Ruby'),
        (TOPIC_GOLANG, 'Golanfg'),
        (TOPIC_SQL, 'SQL'),
        (TOPIC_SWIFT, 'Swift'),
        (TOPIC_PHP, 'PHP'),
        (TOPIC_DELPHI, 'Delphi'),
        (TOPIC_PERL, 'Perl')
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=FULL_NAME_MAX_LENGTH
    )
    topic = models.CharField(
        max_length = FULL_NAME_MAX_LENGTH,
        verbose_name='Предмет',
        choices = TOPIC_CHOICES,
        default = TOPIC_JAVA
    )
    students = models.ManyToManyField(
        Student
    )
    def __str__(self) -> str:
        return f'Профессор: {self.full_name}, Топик: {self.topic}'
    
    def save(self,
        *args: tuple,
        **kwargs: dict
        ) -> None:
        if self.full_name.__len__() > self.FULL_NAME_MAX_LENGTH:
            self.full_name= self.FULL_NAME_MAX_LENGTH
            raise ValidationError(
                f'Допустимый размер строки : {self.FULL_NAME_MAX_LENGTH}'
            )
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = (
            'full_name',
            'topic',
        )
        verbose_name = 'Преподователь'
        verbose_name_plural = 'Преподователи'