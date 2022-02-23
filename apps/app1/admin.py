from typing import Optional
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpRequest
from . models import Account
from . models import Group
from . models import Student
from . models import Professor

class AccountAdmin(admin.ModelAdmin):
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
    )

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Account] = None
    ) -> tuple:
        if obj:
            return self.readonly_fields + ('description',)
        return self.readonly_fields


class GroupAdmin(admin.ModelAdmin):
    readonly_fields = (
        'Group.datetime_created'
        'Group.datetime_deleted'
        'datetime_created',
        'datetime_update',
        'datetime_deleted',
        )


class GroupAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):

    MAX_STUDENT_EDITABLE_AGE = 18
    readonly_fields = (
        'datetime_created',
        'datetime_updated',
        'datetime_deleted',
        )
    list_filter = (
        'age',
        'gpa',
    )
    search_filter = (
        'account_full_name',
    )
    list_display = (
        'age',
        'gpa',
    )
    STUDENT_MAX_AGE = 16

    def student_age_validation(
        self,
        obj: Optional[Student]
    ) -> tuple:
        if obj and obj.age <= self.STUDENT_MAX_AGE:
            return True
        return False

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Student] = None
    ) -> tuple:

        result: bool = self.student_age_validation(obj)
        if result:
            return self.readonly_fields + ('age',)
        return self.readonly_fields

class ProfessorAdmin(admin.ModelAdmin):
    pass

admin.site.register(
    Account,AccountAdmin
)

admin.site.register(
    Group, GroupAdmin
    )

admin.site.register(
    Student, StudentAdmin
    )

admin.site.register(
    Professor, ProfessorAdmin
)