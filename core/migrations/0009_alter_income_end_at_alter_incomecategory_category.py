# Generated by Django 5.1.4 on 2024-12-25 03:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_income_end_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='end_at',
            field=models.DateField(blank=True, db_index=True, default=datetime.datetime(2025, 1, 24, 3, 25, 28, 303271, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='incomecategory',
            name='category',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, unique=True),
        ),
    ]