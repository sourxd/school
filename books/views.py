from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from users.models import User, Students, Cgroup, Ranks
from users.forms import GradesForm
from users.services import *

import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def index(request):
    context = {
        'title': title() + ' - Главная страница',
    }
    return render(request, 'books/index.html', context)


def schedule(request):
    context = {
        'title': title() + ' - Расписание',
    }
    return render(request, 'books/schedule.html', context)


@login_required
def book(request):
    context = {
        'title': title() + ' - Журнал',
    }
    return render(request, 'books/book.html', context)


@login_required
def teach_room(request):
    """ Главная страница учительской """
    class_list = sorted([(cl.clas, cl.group, cl.id) for cl in Cgroup.objects.all()])
    context = {
        'title': title() + ' - Учительская',
        'class_list': class_list,
    }
    return render(request, 'books/teach_room.html', context)


def list_student(request, class_id):
    """ Страница списка учеников """
    stud_list = [(i, stud) for i, stud in
                 enumerate(Students.objects.filter(cgroup_id=class_id).order_by('last_name', 'first_name'),
                           start=1)]

    context = {
        'title': title() + ' - Список учеников',
        'list': stud_list,
        'class_id': class_id,
        'month_id': date.today().month if not 5 < date.today().month < 9 else 9,
    }
    return render(request, 'books/list_student.html', context)


def student_page(request, class_id, students_id, month_id):
    """ Страница оценок ученика, с выбором месяца в шаблоне """
    try:
        student = Students.objects.get(id=students_id)
        cls_num = student.cgroup.clas
        cls_lit = student.cgroup.group
    except:
        return HttpResponseRedirect(reverse('teach_room'))

    rank_in_month = Ranks.objects.filter(student=students_id, date__month=month_id)
    main_dict = {}
    for s in Cgroup.objects.get(clas=cls_num, group=cls_lit).subjects.all():
        dict_days = get_dict_day(month_id)
        temp = {i.date: i.rank for i in rank_in_month.filter(subject=s)}
        dict_days.update(temp)
        main_dict.update({s: list(dict_days.values())})

    context = {
        'title': title() + ' - Информация об ученике',
        'class_id': class_id,
        'student': student,
        'cls_num': cls_num,
        'cls_lit': cls_lit,
        'select_month': select_month()[month_id],
        'list_month': select_month,
        'main_dict': main_dict,
        'long_month': True if len(get_dict_day(month_id)) > 30 else False,
    }
    return render(request, 'books/student_page.html', context)


@login_required
def grades(request, class_id):
    """ Страница выставления оценок ученикам """
    subj_list = User.objects.get(username=request.user.username).subject.all()  # список предметов этого преподавателя
    stud_list = Students.objects.filter(cgroup_id=class_id).order_by('last_name', 'first_name')
    class_subj_list = Cgroup.objects.get(id=class_id).subjects.all()  # список предметов класса
    form = GradesForm(class_subj_list & subj_list, stud_list, initial=request.POST)
    last_marks = Ranks.objects.filter(subject__in=class_subj_list & subj_list).order_by('-id')[:10]

    def processing_post(req):
        form = GradesForm(class_subj_list & subj_list, stud_list, data=req.POST)
        if form.is_valid():
            request.session['form_values'] = req.POST
            dt = form.cleaned_data['date']
            student = form.cleaned_data['student']
            subject = form.cleaned_data['subject']
            rank = form.cleaned_data['rank']
            current_mark = Ranks.objects.filter(date=dt, student=student, subject=subject)
            if 'create_mark' in req.POST:
                if not current_mark:
                    new_rank = Ranks(date=dt, student=student, subject=subject, rank=rank)
                    new_rank.save()
                    messages.success(request, 'Оценка выставлена')
                else:
                    messages.error(request, 'У ученика уже есть оценка.')
            elif 'remove_mark' in req.POST:
                if current_mark:
                    current_mark.delete()
                    messages.success(request, 'Оценка удалена')
                else:
                    messages.error(request, 'Нет оценки за эту дату')

    if request.method == 'POST':
        processing_post(request)

    context = {
        'title': title() + ' - Выставление оценок',
        'form': form,
        'class_id': class_id,
        'last_marks': last_marks,
    }
    return render(request, 'books/grades.html', context)
