# Generated by Django 2.0.6 on 2018-06-15 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0003_auto_20180615_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='awayteam_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='hometeam_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='matchstatistic',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
