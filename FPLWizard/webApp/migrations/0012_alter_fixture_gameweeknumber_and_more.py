# Generated by Django 4.1.1 on 2023-01-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0011_remove_team_leaguepos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fixture',
            name='gameweekNumber',
            field=models.IntegerField(verbose_name='Gameweek'),
        ),
        migrations.AlterField(
            model_name='xpgameweek',
            name='gameweekNumber',
            field=models.IntegerField(verbose_name='Gameweek'),
        ),
        migrations.DeleteModel(
            name='Gameweek',
        ),
    ]