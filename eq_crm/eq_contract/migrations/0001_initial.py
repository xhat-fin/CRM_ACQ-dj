# Generated by Django 5.2.1 on 2025-05-23 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EqContracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_num', models.CharField(max_length=20, unique=True)),
                ('acc_num', models.CharField(max_length=28, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('commission', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('date_add', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='EqTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_transaction', models.DateTimeField(auto_now_add=True)),
                ('sum_transaction', models.DecimalField(decimal_places=2, max_digits=12)),
                ('num_card', models.IntegerField()),
            ],
        ),
    ]
