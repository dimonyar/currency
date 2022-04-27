# Generated by Django 4.0.2 on 2022-04-22 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_from', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('code_name', models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank'), (3, 'vkurse.dp.ua')], unique=True)),
                ('url', models.CharField(max_length=255)),
                ('social', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.FileField(blank=True, default=None, null=True, upload_to='bank_logo')),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro'), ('BTC', 'Bitcoin'), ('UAH', 'Hryvnia')], max_length=5)),
                ('base_type', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro'), ('BTC', 'Bitcoin'), ('UAH', 'Hryvnia')], default='UAH', max_length=5)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('buy', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale', models.DecimalField(decimal_places=2, max_digits=10)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.source')),
            ],
        ),
    ]
