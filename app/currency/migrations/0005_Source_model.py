# Generated by Django 4.0.2 on 2022-03-18 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0004_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('source_url', models.CharField(max_length=255)),
                ('fitch_ratings', models.CharField(max_length=10)),
                ('social_items', models.CharField(max_length=255)),
            ],
        ),
    ]
