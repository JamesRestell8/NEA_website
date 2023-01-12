# Generated by Django 4.1.1 on 2023-01-11 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0014_delete_timemanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerTeamAndPosition',
            fields=[
                ('playerID', models.IntegerField(primary_key=True, serialize=False, verbose_name='Player ID')),
                ('teamID', models.IntegerField(verbose_name='Team ID')),
                ('position', models.IntegerField(verbose_name='Position')),
            ],
        ),
        migrations.DeleteModel(
            name='PlayerTeam',
        ),
    ]