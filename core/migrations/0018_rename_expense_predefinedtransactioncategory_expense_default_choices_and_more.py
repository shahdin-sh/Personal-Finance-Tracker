# Generated by Django 5.1.4 on 2024-12-27 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predefinedtransactioncategory',
            old_name='expense',
            new_name='expense_default_choices',
        ),
        migrations.RenameField(
            model_name='predefinedtransactioncategory',
            old_name='income',
            new_name='income_default_choices',
        ),
    ]