# Generated by Django 2.0.6 on 2018-06-15 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subcriber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcriber',
            name='first_name',
            field=models.CharField(default='', max_length=15),
            preserve_default=False,
        ),
    ]
