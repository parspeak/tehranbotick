from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User
from django.contrib.auth.models import Group


# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['phone_number', 'first_name', 'last_name', 'is_admin']
    list_filter = ['is_admin']
    fieldsets = [
        (None, {'fields': ['phone_number', 'password', 'otp', 'otp_expiry']}),
        ('Personal info', {'fields': ['first_name', 'last_name']}),
        ('Permissions', {'fields': ['is_admin', 'is_active']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['phone_number', 'first_name', 'last_name', 'password', 'confirm_password'],
            },
        ),
    ]
    search_fields = ['first_name', 'last_name']
    ordering = ['first_name']
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
