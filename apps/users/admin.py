from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserRegistrationForm


class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UserRegistrationForm
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_email_verified']
    list_filter = ['is_active', 'username']
    fieldsets = (
        ('Credentials', {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_email_verified')}),
    )


admin.site.register(User, CustomUserAdmin)