# Generated by Django 5.1.4 on 2024-12-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_predefinedtransactioncategory_income_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predefinedtransactioncategory',
            name='expense_category',
            field=models.CharField(blank=True, choices=[('rent', 'Rent'), ('utilities', 'Utilities'), ('groceries', 'Groceries'), ('transportation', 'Transportation'), ('insurance', 'Insurance'), ('entertainment', 'Entertainment'), ('health_medical', 'Health & Medical'), ('education', 'Education'), ('debt_repayment', 'Debt Repayment'), ('savings_investments', 'Savings & Investments'), ('clothing', 'Clothing'), ('personal_care', 'Personal Care'), ('childcare', 'Childcare'), ('charity_donations', 'Charity & Donations'), ('subscriptions', 'Subscriptions'), ('business_expenses', 'Business Expenses'), ('taxes', 'Taxes'), ('gifts_donations', 'Gifts & Donations'), ('travel', 'Travel')], max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='predefinedtransactioncategory',
            name='income_category',
            field=models.CharField(blank=True, choices=[('investmnet', 'Investment'), ('freelance', 'Freelance'), ('job', 'Job')], max_length=200, null=True, unique=True),
        ),
    ]