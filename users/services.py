from calendar import monthrange
from datetime import date
import datetime


def select_month():
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


def title():
    return 'Школа №999'


def get_datetime_range(year, month):
    nb_days = monthrange(year, month)[1]
    dict_date = {datetime.date(year, month, day): '' for day in range(1, nb_days + 1)}
    return dict_date


def get_dict_day(month_id):
    current_date = date.today()
    if date.today().month < 6 and month_id > 8:
        dict_days = get_datetime_range(current_date.year - 1, month_id)
    else:
        dict_days = get_datetime_range(current_date.year, month_id)
    return dict_days
