# Generated by Django 4.0.2 on 2022-05-16 19:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_alter_source_code_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]