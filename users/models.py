from django.db import models
from django.contrib.auth.models import AbstractUser


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
    clas = models.IntegerField(help_text='Название класса')
    group = models.CharField(max_length=255, help_text='Буква класса (А-Я) на русском языке')
    ceo = models.ForeignKey(verbose_name='Классный руководитель', to=User, on_delete=models.DO_NOTHING, default=None, null=True)

    def __str__(self):
        return f'{self.clas}{self.group}'

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'


class Subjects(models.Model):
    subj = models.CharField(max_length=255, help_text='Название предмета')

    def __str__(self):
        return self.subj

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Students(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(verbose_name='Дата рождения')
    cgroup = models.ForeignKey('Cgroup', on_delete=models.DO_NOTHING, default=None)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
