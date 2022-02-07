from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.contrib import admin

from . models import Account 
from. models import Group
from. models import Student


class AccountAdmin(admin.ModelAdmin):

    readonly_fields = ()

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Account] = None
    ) -> tuple:

        if obj:
            return self.readonly_fields + ('description',)
        return self.readonly_fields

class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ()
  

class StudentAdmin(admin.ModelAdmin):
    STUDENT_EDIT_MAX_AGE = 16

    readonly_fields = ()

    def student_age_validation(
        self,
        obj:Student
    ) -> tuple:
        if obj and obj.age <= self.STUDENT_EDIT_MAX_AGE:
            return self.readonly_fields + ('age',)
        return self.readonly_fields


    def student_age_validation_2(
        self,
        obj:Student
    ) -> bool:
        if obj and obj.age <= self.STUDENT_EDIT_MAX_AGE:
            return True
        return False

    def get_readonly_fields(
        self,
        request: WSGIRequest,
        obj: Optional[Student] = None
    ) -> tuple:

        result: tuple = self.student_age_validation(obj)
        return result


admin.site.register(
    Account, AccountAdmin
)
admin.site.register(
    Group, GroupAdmin
)
admin.site.register(
    Student, StudentAdmin
)
