# Generated by Django 4.1.1 on 2022-11-15 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0002_timemanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fplapistatsgameweek',
            name='fpl_ppg',
        ),
        migrations.AddField(
            model_name='fplapistatsgameweek',
            name='fpl_fixtureID',
            field=models.IntegerField(default=0, verbose_name='Fixture Number'),
        ),
        migrations.AddField(
            model_name='fplapistatsgameweek',
            name='fpl_gameweekNumber',
            field=models.IntegerField(default=0, verbose_name='Gameweek Number'),
        ),
    ]
