from django.contrib.auth import get_user_model, login, authenticate, logout
from django.shortcuts import render, redirect

from web.forms import RegistrationForm, AuthForm

User = get_user_model()

def index(request):
    return render(request, "web/main.html")

def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            return redirect('main')

    return render(request, 'web/registration.html', {'form': form})


def login_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)

                return redirect('main')

    return render(request, 'web/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')