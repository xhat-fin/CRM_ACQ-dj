# Generated by Django 5.2.1 on 2025-05-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eq_contract', '0003_eqtransactions_sum_commission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eqtransactions',
            name='num_card',
            field=models.CharField(),
        ),
    ]
