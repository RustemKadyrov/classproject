from django import forms
from app1.models import Homework, File
from apps.auths import forms

class HomeworkForm(forms.ModelForm):
    title = forms.CharField(label='Оглавление')
    subject = forms.CharField(

    )

    class Meta:
        model = Homework
        fields = (
            'title',
            'subject',
        )

class FileForm(forms.ModelForm):
    title = forms.CharField(label='Оглавление')
    obj = forms.FileField(

    )

    class Meta:
        model = File
        fields = (
            'title',
            'obj',
        )