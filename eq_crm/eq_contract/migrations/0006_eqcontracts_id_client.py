# Generated by Django 5.2.1 on 2025-05-24 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('eq_contract', '0005_alter_eqcontracts_date_add'),
    ]

    operations = [
        migrations.AddField(
            model_name='eqcontracts',
            name='id_client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='clients.clients'),
            preserve_default=False,
        ),
    ]
