from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


# TODO: Add custom filters if its needed
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ('username' ,'email', 'first_name', 'last_name', 'get_status', 'get_groups')
    list_per_page = 10
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username' ,'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None, 
            {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser','is_active'),
            }
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)

    @admin.display(description='status')
    def get_status(self, obj):
        if obj.is_superuser:
            return 'superuser'
        if obj.is_staff:
            return 'staffuser'
        return 'user'

    @admin.display(description='groups')
    def get_groups(self, obj):
        return ','.join([group.name for group in obj.groups.all()])
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('groups')


admin.site.register(CustomUser, CustomUserAdmin)
