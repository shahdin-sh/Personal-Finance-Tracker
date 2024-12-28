from django.contrib import admin
from django.db.models import Prefetch, Count
from .models.transaction_models import PredefinedTransactionCategory, TransactionCategory, Transaction


class PredefinedTransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'type']
    list_filter = ['type']
    readonly_fields = ['type']
    ordering = ['type']

    @admin.display(description='name')
    def get_name(self, obj):
        if obj.income_category:
            return obj.income_category
        return obj.expense_category

    def has_delete_permission(self, request, obj=None):
        return False


class TransactionInline(admin.TabularInline):
    model = Transaction
    fields = ['user', 'type', 'clean_amount'] 
    readonly_fields = ['user' ,'type', 'clean_amount']
    show_change_link = False # Disable count query for related items 

    @admin.display(description='amount')
    def clean_amount(self, obj):
        return obj.clean_amount
    
    def has_add_permission(self, request, obj):
        return False
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'source__predefined_category')


class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['get_category', 'type']
    search_fields = ('category', 'predefined_category')
    list_filter = ('type', 'is_shared')
    ordering = ['type']
    inlines = [
        TransactionInline
    ]

    @admin.display(description='category')
    def get_category(self, obj):
        if obj.category:
            return obj.category
        return obj.predefined_category
    
    @admin.display(description='users')
    def get_users(self, obj):
        return obj.users.count()
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('predefined_category')
 

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'source', 'type', 'clean_amount', 'end_at', 'currency']
    autocomplete_fields = ['source'] # dynamically loading related records only when needed, reducing query count.
    list_per_page = 10
    list_filter = ['user', 'type', 'currency']
    ordering = ['user__username']

    @admin.display(description='amount')
    def clean_amount(self, obj):
        return obj.clean_amount

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'source__predefined_category').prefetch_related('source__users')


admin.site.register(PredefinedTransactionCategory, PredefinedTransactionCategoryAdmin)
admin.site.register(TransactionCategory, TransactionCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)