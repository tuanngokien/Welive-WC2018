# Generated by Django 2.0.6 on 2018-06-15 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0002_auto_20180615_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='awayteam_name',
            new_name='awayteam',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='hometeam_name',
            new_name='hometeam',
        ),
    ]
