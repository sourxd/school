from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.models import User, Students
from users.forms import ChClassForm
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


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


def teach_room(request):
    if not User.objects.filter(username=request.user.username, is_teacher=True):
        return HttpResponseRedirect(reverse('index'))
    context = {
        'title': 'Школа №999 - Учительская',
    }
    return render(request, 'books/teach_room.html', context)

def list_student(request):
    stud_list = None
    form = ChClassForm()
    if request.method == 'POST':
        form = ChClassForm(data=request.POST)
        clas = request.POST['clas']
        if form.is_valid():
            stud_list = [(i, stud) for i, stud in enumerate(Students.objects.filter(cgroup_id=clas).order_by('last_name', 'first_name'), start=1)]
    context = {
        'title': 'Школа №999 - Список учеников',
        'form': form,
        'list': stud_list,
    }
    return render(request, 'books/list_student.html', context)

def student_page(request, students_id):
    try:
        student = Students.objects.get(id=students_id)
    except:
        return HttpResponseRedirect(reverse('list_student'))
    context = {
        'title': 'Школа №999 - Информация об ученике',
        'student': student,
    }
    return render(request, 'books/student_page.html', context)
