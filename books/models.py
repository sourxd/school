from django.db import models

import datetime


class Subjects(models.Model):
    subj = models.CharField(max_length=255, verbose_name='Название предмета')

    def __str__(self):
        return self.subj

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Cgroup(models.Model):
    clas = models.IntegerField(help_text='Целое число 1-11', verbose_name='Класс')
    group = models.CharField(max_length=255, help_text='Буква класса (А-Я) на русском языке', verbose_name='Литера')
    ceo = models.ForeignKey(to='users.User', on_delete=models.DO_NOTHING, verbose_name='Классный руководитель',
                            default=None,
                            null=True)
    subjects = models.ManyToManyField('Subjects', default=None, verbose_name='Предметы у класса')

    def __str__(self):
        return f'{self.clas}{self.group}'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Students(models.Model):
    SEX_CHOICES = (
        ('М', 'М',),
        ('Ж', 'Ж',),
    )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name='Пол')
    birth_date = models.DateField(verbose_name='Дата рождения')
    cgroup = models.ForeignKey(to=Cgroup, on_delete=models.DO_NOTHING, default=None, verbose_name='Класс')
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
    teacher = models.ForeignKey(to='users.User', on_delete=models.CASCADE, verbose_name='Преподаватель', editable=False)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'{self.date}, {self.student}, {self.subject}, {self.rank}'


class Daylessons(models.Model):
    date = models.DateField(default=datetime.date.today, verbose_name='Дата')
    group = models.ForeignKey(to=Cgroup, on_delete=models.CASCADE, verbose_name='Класс')
    first = models.CharField(max_length=25, verbose_name='1', null=True, blank=True)
    second = models.CharField(max_length=25, verbose_name='2', null=True, blank=True)
    third = models.CharField(max_length=25, verbose_name='3', null=True, blank=True)
    fourth = models.CharField(max_length=25, verbose_name='4', null=True, blank=True)
    fifth = models.CharField(max_length=25, verbose_name='5', null=True, blank=True)
    sixth = models.CharField(max_length=25, verbose_name='6', null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')

    class Meta:
        verbose_name = 'Расписание на день'
        verbose_name_plural = 'Расписание'
