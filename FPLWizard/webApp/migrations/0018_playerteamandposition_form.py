# Generated by Django 4.1.1 on 2023-01-12 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0017_remove_fplapistatsgameweek_fpl_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerteamandposition',
            name='form',
            field=models.FloatField(default=0, verbose_name='Form'),
            preserve_default=False,
        ),
    ]
