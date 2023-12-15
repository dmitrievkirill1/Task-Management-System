from django.contrib.auth import get_user_model
from django import forms

from web.models import Project, Task, Comment

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password2', 'Пароли не совпадают')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class TaskForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Новая', 'Новая'),
        ('В процессе', 'В процессе'),
        ('Завершена', 'Завершена'),
    ]

    status = forms.ChoiceField(label='Статус', choices=STATUS_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status']
        widgets = {
            "deadline": forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class TaskFilterForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Поиск'}), required=False)
    is_comment = forms.NullBooleanField(
        label='',
        widget=forms.Select(
            choices=(
                ('unknown', 'Наличие комментариев.'),
                ('true', 'Комментарии есть.'),
                ('false', 'Комментариев нет.'),
            )
        )
    )
