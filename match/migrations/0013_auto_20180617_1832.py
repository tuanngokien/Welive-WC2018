# Generated by Django 2.0.6 on 2018-06-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0012_auto_20180617_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(blank=True, default='', max_length=8),
        ),
    ]
