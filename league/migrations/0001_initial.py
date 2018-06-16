# Generated by Django 2.0.6 on 2018-06-15 16:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('en_name', models.CharField(max_length=10)),
                ('vi_name', models.CharField(max_length=10)),
            ],
        ),
    ]
