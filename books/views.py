from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.models import User


def index(request):
    context = {
        'title': 'Школа №999 - Главная страница',
    }
    return render(request, 'books/index.html', context)


def schedule(request):
    context = {
        'title': 'Школа №999 - Расписание',
    }
    return render(request, 'books/schedule.html', context)


@login_required
def book(request):
    context = {
        'title': 'Школа №999 - Журнал',
    }
    return render(request, 'books/book.html', context)


@login_required
def teach_room(request):
    print(request.user.groups)
    if not request.user.last_name:
        return HttpResponseRedirect(reverse('index'))
    context = {
        'title': 'Школа №999 - Учительская',
    }
    return render(request, 'users/registration.html', context)
