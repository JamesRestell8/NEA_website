# Generated by Django 4.1.1 on 2022-11-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0003_remove_fplapistatsgameweek_fpl_ppg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiiddictionary',
            name='fplName',
            field=models.CharField(default='Null', max_length=100, verbose_name='FPL Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apiiddictionary',
            name='understatName',
            field=models.CharField(default='Null', max_length=100, verbose_name='Understat Name'),
            preserve_default=False,
        ),
    ]