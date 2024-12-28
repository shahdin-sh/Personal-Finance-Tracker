# Generated by Django 5.1.4 on 2024-12-28 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_rename_user_transactioncategory_users'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predefinedtransactioncategory',
            old_name='transaction_type',
            new_name='type',
        ),
        migrations.AddField(
            model_name='transactioncategory',
            name='type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], default='income', max_length=200),
        ),
    ]
