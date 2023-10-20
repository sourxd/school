from django.db import models
from django.contrib.auth.models import AbstractUser

from books.models import Subjects


class User(AbstractUser):
    is_editor = models.BooleanField(default=False, verbose_name='Статус редактора')
    is_teacher = models.BooleanField(default=False, verbose_name='Статус учителя')
    subject = models.ManyToManyField(to=Subjects, default=None, verbose_name='Ведет предметы')
    patronymic = models.CharField(max_length=25, verbose_name='Отчество')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
