from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def login(request):
    """ Страница входа """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Вход'
    }
    return render(request, 'users/login.html', context)


def registration(request):
    """ Страница регистрации пользователя """
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('login'))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        form = UserRegistrationForm()
    context = {
        'form': form,
        'title': 'Регистрация',
    }
    return render(request, 'users/registration.html', context)


def logout(request):
    """ Выход из аккаунта """
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
