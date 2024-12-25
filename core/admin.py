from django.contrib import admin
from .models import IncomeCategory, Income, PredefinedIncomeCategory

# Income Inclines and Admin Models
class PredefinedIncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_delete_permission(self, request, obj=None):
        return False

  
class IncomeInline(admin.TabularInline):
    model = Income
    fields = ['user', 'type', 'clean_amount'] 
    readonly_fields = ['user' ,'type', 'clean_amount']

    @admin.display(description='amount')
    def clean_amount(self, obj):
        return obj.clean_amount
    
    def has_add_permission(self, request, obj):
        return False


class IncomeCategoryAdmin(admin.ModelAdmin):
    list_display = ['get_category']
    search_fields = ('category', 'predefined_category')
    list_filter = ('category', 'predefined_category')
    # ordering = ['user__username']
    inlines = [
        IncomeInline
    ]

    @admin.display(description='category')
    def get_category(self, obj):
        if obj.category:
            return obj.category
        return obj.predefined_category
 

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['user', 'source', 'type', 'clean_amount', 'end_at', 'currency']
    list_per_page = 10
    ordering = ['user__username']

    @admin.display(description='amount')
    def clean_amount(self, obj):
        return obj.clean_amount


admin.site.register(PredefinedIncomeCategory, PredefinedIncomeCategoryAdmin)
admin.site.register(IncomeCategory, IncomeCategoryAdmin)
admin.site.register(Income, IncomeAdmin)