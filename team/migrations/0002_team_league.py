# Generated by Django 2.0.6 on 2018-06-15 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('league', '0003_auto_20180615_1707'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='league',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='league.League'),
            preserve_default=False,
        ),
    ]
