from .imports import *


class PredefinedIncomeCategory(models.Model):
    # this list will updated later 
    DEFAULT_CHOICES = [
        ('job', 'Job'),
        ('investment', 'Investment'),
        ('freelance', 'Freelance'),
    ]

    name = models.CharField(max_length=200, choices=DEFAULT_CHOICES, unique=True)

    def __str__(self):
        return self.name
       

class IncomeCategory(models.Model):
    category = models.CharField(max_length=200, blank=True, null=True, db_index=True, unique=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='income_categories')
    predefined_category = models.OneToOneField(
        "PredefinedIncomeCategory", 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
    )

    def __str__(self):
        return self.category if self.category else str(self.predefined_category)
     
    def _validate_category_fields(self):
        if self.category and self.predefined_category:
            raise ValidationError('You can only choose predefined categories or create a category.')
        
        if self.category in dict(PredefinedIncomeCategory.DEFAULT_CHOICES).keys():
            raise ValidationError(f'{self.category}: Choose entered category in predefined_category field.')
        
    def clean(self):
        self._validate_category_fields()


class Income(models.Model):

    TOMAN_MIN_AMOUNT = 100000
    DOLLAR_MIN_AMOUNT = 10
    
    INCOME_TYPE_CHOICES = [
        ('recurring', 'RECURRING'),
        ('one-time', 'ONE-TIME')
    ]

    CURRENCY_CHOICES = [
        ('toman', 'TOMAN'),
        ('dollar', 'USD'),
    ]


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incomes', db_index=True)
    source = models.ForeignKey("IncomeCategory", on_delete=models.CASCADE, related_name='incomes', db_index=True)
    type = models.CharField(max_length=200, choices=INCOME_TYPE_CHOICES, default=INCOME_TYPE_CHOICES[0])
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=200, choices=CURRENCY_CHOICES, default=CURRENCY_CHOICES[0], db_index=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'source']

    def __str__(self):
        return f'{self.user} | {self.source}'
    
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
                raise ValidationError({'amount': f'The minimum amount for Toman is {self.TOMAN_MIN_AMOUNT: ,}.'})
            if self.currency == self.CURRENCY_CHOICES[1][0] and self.amount < self.DOLLAR_MIN_AMOUNT:
                raise ValidationError({'amount': f'The minimum amount for Dollar is {self.DOLLAR_MIN_AMOUNT}.'})
    
    def _validate_ending_time_method(self):
        if self.type:
            if self.type == self.INCOME_TYPE_CHOICES[1][0] and self.end_at:
                raise ValidationError({'end_at': 'Income ending timeline only occur when income type is recurring.'})
            if self.type == self.INCOME_TYPE_CHOICES[0][0] and not self.end_at:
                self.end_at = now() + timedelta(days=30)
    
    def _validate_user_association_with_source(self):
        if self.source:
            if not self.source.user.filter(id=self.user.id).exists():
                raise ValidationError("The user is not associated with the selected income category.")
    
    
    def clean(self): # work outside the admin panel requires calling instance.full_clean()
       self._validate_currency_method()
       self._validate_ending_time_method()
       self._validate_user_association_with_source()