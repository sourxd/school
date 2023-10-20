from django.shortcuts import render
from django.views import View

from books.forms import ScheduleForm, AddStudentForm
from books.services import *

from books.forms import GradesForm
from users.models import User
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


class IndexPageView(View):
    """ Главная страница """

    def get(self, request):
        return render(request, 'books/index.html', {'title': title() + ' - Главная страница'})


class ScheduleView(View):
    """ Страница с расписанием """

    def get(self, request):
        return render(request, 'books/schedule.html', {'title': title() + ' - Расписание', 'form': ChClassForm()})

    def post(self, request):
        form = ChClassForm(data=request.POST)  # выбираем класс.
        schedule_list = get_schedule(request)  # получаем сортированный по date список с расписанием на неделю
        context = {
            'title': title() + ' - Расписание',
            'form': form,
            'schedule_list': schedule_list,
        }
        return render(request, 'books/schedule.html', context)


class TeachRoomView(View):
    """ Главная страница журнала """

    def get(self, request):
        return render(request, 'books/teach_room.html',
                      {'title': title() + ' - Журналы', 'class_list': get_list_classes()})


class StudentPageView(View):
    """ Страница оценок ученика, с выбором месяца в шаблоне """

    def get(self, request, class_id, students_id, month_id):
        student = safe_filter(Students, id=students_id)[0]  # выбранный ученик
        rank_in_month = safe_filter(Ranks, student=students_id, date__month=month_id)
        main_dict = get_marks_dict(students_id, month_id, rank_in_month)  # итоговый dict с оценками за месяц по date
        context = {
            'title': title() + ' - Информация об ученике',
            'class_id': class_id,
            'student': student,
            'select_month': select_month()[month_id],
            'list_month': select_month(),
            'main_dict': main_dict,
            'long_month': True if len(get_dict_day(month_id)) > 30 else False,
        }
        return render(request, 'books/student_page.html', context)


class GradesView(View):
    """ Страница выставления оценок ученикам """

    def get(self, request, class_id):
        subj_list = safe_filter(User, username=request.user.username)[0].subject.all()  # список предметов этого User
        stud_list = safe_filter(Students, cgroup_id=class_id).order_by('last_name', 'first_name')
        class_subj_list = safe_filter(Cgroup, id=class_id)[0].subjects.all()  # список предметов класса
        form = GradesForm(class_subj_list & subj_list, stud_list, initial=request.POST)
        last_marks = safe_filter(Ranks, teacher=request.user.id).order_by('-id')[:10]  # 10 последних выст. оценок
        context = {
            'title': title() + ' - Выставление оценок',
            'form': form,
            'class_id': class_id,
            'last_marks': last_marks,
        }
        return render(request, 'books/grades.html', context)

    def post(self, request, class_id):
        subj_list = filter_objects(User, username=request.user.username)[0].subject.all()  # список предметов этого User
        stud_list = filter_objects(Students, cgroup_id=class_id).order_by('last_name', 'first_name')
        class_subj_list = filter_objects(Cgroup, id=class_id)[0].subjects.all()  # список предметов класса
        form = GradesForm(class_subj_list & subj_list, stud_list, data=request.POST)
        last_marks = filter_objects(Ranks, teacher=request.user.id).order_by('-id')[:10]  # 10 последних выст. оценок

        if form.is_valid():
            request.session['form_values'] = request.POST
            form.cleaned_data['teacher'] = safe_filter(User, id=request.user.id)[0]
            current_mark_value = current_mark(form.cleaned_data)
            msg = {
                False: {True: 'Оценка выставлена', False: 'У ученика уже есть оценка.'},
                True: {True: 'Оценка удалена', False: 'Нет оценки за эту дату'}
            }
            add_remove_func(Ranks, request, form.cleaned_data, current_mark_value, msg)

        context = {
            'title': title() + ' - Выставление оценок',
            'form': form,
            'class_id': class_id,
            'last_marks': last_marks,
        }
        return render(request, 'books/grades.html', context)


class ListStudentView(View):
    """ Страница списка учеников """

    def get(self, request, class_id):
        stud_list = [(i, n) for i, n in
                     enumerate(safe_filter(Students, cgroup_id=class_id).order_by('last_name', 'first_name'),
                               start=1)]  # список учеников выбранного класса
        context = {
            'title': title() + ' - Список учеников',
            'list': stud_list,
            'class_id': class_id,
            'month_id': date.today().month if not 5 < date.today().month < 9 else 9,
        }
        return render(request, 'books/list_student.html', context)


class EditorView(View):
    """ Редактирование расписания """

    def get(self, request, class_id):
        list_subj = safe_filter(Cgroup, id=class_id)[0].subjects.all()  # доступные предметы для этого класса
        form = ScheduleForm(list_subj)

        context = {
            'title': title() + ' - Редактирование расписания',
            'class_id': class_id,
            'form': form,
            'today_schedule': None,
        }
        return render(request, 'books/edit.html', context)

    def post(self, request, class_id):
        list_subj = safe_filter(Cgroup, id=class_id)[0].subjects.all()  # доступные предметы для этого класса
        today_schedule = None
        form = ScheduleForm(list_subj, data=request.POST)
        msg = {
            False: {True: 'Сохранено!', False: 'Расписание на эту дату уже есть'},
            True: {True: 'Расписание за этот день удалено', False: 'Нет расписания на этот день'}
        }
        if form.is_valid():
            date = form.cleaned_data['date']
            form.cleaned_data['group_id'] = class_id
            check_schedule = filter_objects(Daylessons, date=date, group_id=class_id)
            today_schedule = add_remove_func(Daylessons, request, form.cleaned_data, check_schedule, msg, True)

        context = {
            'title': title() + ' - Редактирование расписания',
            'class_id': class_id,
            'form': form,
            'today_schedule': today_schedule,
        }
        return render(request, 'books/edit.html', context)


class AddStudentView(View):
    """ Страница добавления нового ученика """

    def get(self, request, class_id):
        return render(request, 'books/add_student.html',
                      {'title': title() + ' - Добавление ученика', 'form': AddStudentForm(class_id),
                       'class_id': class_id})

    def post(self, request, class_id):
        form = AddStudentForm(class_id, data=request.POST)
        if form.is_valid():
            add_students(request, form.cleaned_data)
        context = {
            'title': title() + ' - Добавление ученика',
            'form': form,
            'class_id': class_id,
        }
        return render(request, 'books/add_student.html', context)
