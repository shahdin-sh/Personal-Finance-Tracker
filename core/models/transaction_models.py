from .imports import *


class PredefinedTransactionCategory(models.Model):
    INCOME_DEFAULT_CHOICES = [
        ('investmnet', 'Investment'),
        ('freelance', 'Freelance'),
        ('job', 'Job'),
    ]

    EXPENSE_DEFAULT_CHOICES = [
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('groceries', 'Groceries'),
        ('transportation', 'Transportation'),
        ('insurance', 'Insurance'),
        ('entertainment', 'Entertainment'),
        ('health_medical', 'Health & Medical'),
        ('education', 'Education'),
        ('debt_repayment', 'Debt Repayment'),
        ('savings_investments', 'Savings & Investments'),
        ('clothing', 'Clothing'),
        ('personal_care', 'Personal Care'),
        ('childcare', 'Childcare'),
        ('charity_donations', 'Charity & Donations'),
        ('subscriptions', 'Subscriptions'),
        ('business_expenses', 'Business Expenses'),
        ('taxes', 'Taxes'),
        ('gifts_donations', 'Gifts & Donations'),
        ('travel', 'Travel'),
    ]

    TRANSACTION_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    type = models.CharField(max_length=200, choices=TRANSACTION_CHOICES, blank=True)
    income_category = models.CharField(max_length=200, choices=INCOME_DEFAULT_CHOICES, blank=True, null=True, unique=True)
    expense_category = models.CharField(max_length=200, choices=EXPENSE_DEFAULT_CHOICES, blank=True, null=True, unique=True)

    def __str__(self):
        return self.income_category if self.income_category else self.expense_category
    
    # Overiding the save method because this model will rarely use
    def save(self, *args, **kwargs):
        if self.income_category:
            self.type = self.TRANSACTION_CHOICES[0][0]
        if self.expense_category:
            self.type = self.TRANSACTION_CHOICES[1][0]
        return super().save(*args, **kwargs)
    
    def clean(self):
        if self.income_category and self.expense_category:
            raise ValidationError('A category cannot be both income and expense. Please select only one.')
        
        if not self.income_category and not self.expense_category:
            raise ValidationError('Please select either an income or expense category.')


class TransactionCategory(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    category = models.CharField(max_length=200, blank=True, null=True, db_index=True, unique=True)
    type = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0])
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='transaction_categories')
    predefined_category = models.OneToOneField(
        "PredefinedTransactionCategory", 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
    )
    # TODO: Move is_shared logic to another service file or utility
    is_shared = models.BooleanField(default=False)


    def __str__(self):
        return self.category if self.category else str(self.predefined_category)


class Transaction(models.Model):
    TOMAN_MIN_AMOUNT = 100000
    DOLLAR_MIN_AMOUNT = 10

    TRANSACTION_TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]
    
    PERIOD_TYPE_CHOICES = [
        ('recurring', 'Recurring'),
        ('one-time', 'one-time')
    ]

    CURRENCY_CHOICES = [
        ('toman', 'Toman'),
        ('dollar', 'USD'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', db_index=True)
    source = models.ForeignKey("TransactionCategory", on_delete=models.CASCADE, related_name='transactions', db_index=True)
    type = models.CharField(max_length=200, choices=TRANSACTION_TYPE_CHOICES, default=TRANSACTION_TYPE_CHOICES[0])
    period_type = models.CharField(max_length=200, choices=PERIOD_TYPE_CHOICES, default=PERIOD_TYPE_CHOICES[0])
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=200, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0], db_index=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'source']

    def __str__(self):
        return f'{self.user} | {self.type} | {self.source}'
    
    @property
    def clean_amount(self):
        if self.amount:
            amount = f'{self.amount: ,}'

        if self.currency == self.CURRENCY_CHOICES[0][0]:
            return f'{amount} T'
        return f'{amount} $'
    
    def _validate_currency_method(self):
        if self.currency and self.amount:
            if self.currency == self.CURRENCY_CHOICES[0][0] and self.amount < self.TOMAN_MIN_AMOUNT:
                raise ValidationError({'amount': f'The amount must be at least {self.TOMAN_MIN_AMOUNT:,} for transactions in Toman.'})
            if self.currency == self.CURRENCY_CHOICES[1][0] and self.amount < self.DOLLAR_MIN_AMOUNT:
                raise ValidationError({'amount': f'The amount must be at least {self.DOLLAR_MIN_AMOUNT} for transactions in Dollar.'})
    
    def _validate_ending_time_method(self):
        if self.type == self.PERIOD_TYPE_CHOICES[1][0] and self.end_at:
            raise ValidationError({'end_at': 'End date is only applicable for recurring transactions.'})
     
    def clean(self):
        self._validate_currency_method()
        self._validate_ending_time_method()

