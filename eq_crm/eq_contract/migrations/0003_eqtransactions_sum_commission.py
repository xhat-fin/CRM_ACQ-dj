# Generated by Django 5.2.1 on 2025-05-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eq_contract', '0002_eqtransactions_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='eqtransactions',
            name='sum_commission',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12),
            preserve_default=False,
        ),
    ]
