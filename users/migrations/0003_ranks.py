# Generated by Django 4.2.6 on 2023-10-10 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_cgroup_subjects_alter_user_options_user_is_teacher_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('rank', models.CharField(max_length=1, verbose_name='Б/Н/Оценка')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.subjects', verbose_name='Предмет')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
    ]