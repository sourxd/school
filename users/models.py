import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_teacher = models.BooleanField(('Статус учителя'), default=False,
                                     help_text='Устанавливает данного пользователя учителем')
    subject = models.ManyToManyField('Subjects', default=None, verbose_name='Ведет предметы')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Cgroup(models.Model):
    clas = models.IntegerField(help_text='Целое число 1-11', verbose_name='Класс')
    group = models.CharField(max_length=255, help_text='Буква класса (А-Я) на русском языке', verbose_name='Литера')
    ceo = models.ForeignKey(verbose_name='Классный руководитель', to=User, on_delete=models.DO_NOTHING, default=None,
                            null=True)
    subjects = models.ManyToManyField('Subjects', default=None, verbose_name='Предметы у класса')

    def __str__(self):
        return f'{self.clas}{self.group}'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Subjects(models.Model):
    subj = models.CharField(max_length=255, verbose_name='Название предмета')

    def __str__(self):
        return self.subj

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Students(models.Model):
    SEX_CHOICES = (
        ('М', 'М',),
        ('Ж', 'Ж',),
    )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата рождения')
    cgroup = models.ForeignKey('Cgroup', on_delete=models.DO_NOTHING, default=None, verbose_name='Класс')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Ranks(models.Model):
    LIST_RANK_CHOICES = (
        (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), ('Б', 'Б'), ('Н', 'Н')
    )
    date = models.DateField(verbose_name='Дата получения оценки', default=datetime.date.today)
    student = models.ForeignKey(to=Students, on_delete=models.CASCADE, verbose_name='Ученик')
    subject = models.ForeignKey(to=Subjects, on_delete=models.CASCADE, verbose_name='Предмет')
    rank = models.CharField(max_length=1, choices=LIST_RANK_CHOICES, verbose_name='Б/Н/Оценка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.date}, {self.student}, {self.subject}, {self.rank}'
