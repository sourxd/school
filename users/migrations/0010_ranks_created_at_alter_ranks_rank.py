# Generated by Django 4.2.6 on 2023-10-14 12:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_ranks_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranks',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ranks',
            name='rank',
            field=models.CharField(choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1), ('Б', 'Б'), ('Н', 'Н')], max_length=1, verbose_name='Б/Н/Оценка'),
        ),
    ]