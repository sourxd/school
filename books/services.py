from calendar import monthrange
from datetime import datetime, timedelta, date
from typing import NoReturn

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

from books.forms import ChClassForm
from books.models import Students, Ranks, Daylessons, Cgroup

### Декораторы проверки принадлежности
### Проверка на редактора
editor_required = user_passes_test(lambda u: u.is_editor, login_url=reverse_lazy('index'))

### Проверка на учителя
teacher_required = user_passes_test(lambda u: u.is_teacher, login_url=reverse_lazy('index'))


### Проверка корректности запроса.
def safe_filter(model, **kwargs):
    """ Безопасный фильтр с исключением при пустой выборке """
    try:
        return model.objects.filter(**kwargs)
    except:
        raise IndexError('Ошибка параметров запроса')


def select_month() -> dict:
    """ Список учебных месяцев """
    select_month = {
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь',
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
    }
    return select_month


def title() -> str:
    """ Название в title """
    return 'Школа №999'


def filter_objects(model, **kwargs):
    """ Обычная фильтрация """
    return model.objects.filter(**kwargs)


### Расписание

def get_schedule(request):
    """ Получение расписания для определенного класса на неделю вперед через форму """
    form = ChClassForm(data=request.POST)
    id_class_in_cgroup = request.POST['id'] or 3
    if form.is_valid():
        one_week_later = datetime.today() + timedelta(days=8)
        return filter_objects(Daylessons, group_id=id_class_in_cgroup,
                              date__range=[datetime.today(), one_week_later]).order_by('date')
    raise IndexError


### Журналы

def get_list_classes() -> list:
    """ Список классов tuple(Цифра, Буква, id, Кл. Руководитель) """
    return sorted([(cl.clas, cl.group, cl.id, cl.ceo) for cl in Cgroup.objects.all()])


### Ученики и оценки

def students_filter(**kwargs):
    """ Фильтр по ученикам """
    return Students.objects.filter(**kwargs)


def get_dict_day(month_id: int) -> dict:
    """ Отображение дней месяца/года в зависимости от текущего месяца """

    def get_datetime_range(year: int, month: int) -> dict:
        """ Получение словаря чисел месяца """
        nb_days = monthrange(year, month)[1]
        dict_date = {date(year, month, day): '' for day in range(1, nb_days + 1)}
        return dict_date

    current_date = date.today()
    shift = 0
    if current_date.month < 6 and month_id > 8:
        shift += 1
    return get_datetime_range(current_date.year - shift, month_id)


def get_marks_dict(students_id: int, month_id: int, rank_in_month) -> dict:
    """ Получить словарь с оценками в заданный месяц """
    student = filter_objects(Students, id=students_id)[0]
    main = {}
    for s in filter_objects(Cgroup, clas=student.cgroup.clas, group=student.cgroup.group)[0].subjects.all():
        dict_days = get_dict_day(month_id)
        temp = {i.date: i.rank for i in rank_in_month.filter(subject=s)}
        dict_days.update(temp)
        main.update({s: list(dict_days.values())})
    return main


def current_mark(cleaned_data: dict):
    """ Проверка, есть ли у ученика оценка в этот день по этому предмету """
    return filter_objects(Ranks, date=cleaned_data['date'], student=cleaned_data['student'],
                          subject=cleaned_data['subject'])


def add_remove_func(model, request, cleaned_data: dict, c_value, msg: dict, option: bool = False):
    """ Функция добавления/удаления данных из базы с двумя кнопками с выводом сообщения """
    if 'create' in request.POST:
        if not c_value:
            model.objects.create(**cleaned_data)
            messages.success(request, msg[False][True])
        else:
            messages.error(request, msg[False][False])
        if option:
            return filter_objects(Daylessons, date=cleaned_data['date'], group_id=cleaned_data['group_id'])[0]
    elif 'remove' in request.POST:
        if c_value:
            c_value.delete()
            messages.success(request, msg[True][True])
        else:
            messages.error(request, msg[True][False])


def add_students(request, cleaned_data):
    """ Функция добавления нового ученика из формы """
    Students.objects.create(**cleaned_data)
    return messages.success(request, 'Новый ученик добавлен!')