from django.contrib.auth import get_user_model
from django import forms

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