# Generated by Django 5.2.1 on 2025-05-23 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unp', models.CharField(max_length=18)),
                ('name', models.CharField(max_length=180)),
                ('date_add', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
