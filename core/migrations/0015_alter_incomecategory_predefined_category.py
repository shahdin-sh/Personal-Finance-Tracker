# Generated by Django 5.1.4 on 2024-12-25 04:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_income_end_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomecategory',
            name='predefined_category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.predefinedincomecategory'),
        ),
    ]