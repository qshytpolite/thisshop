from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .form import CustomUserForm
from .models import User

from unfold.admin import ModelAdmin

# admin.site.unregister(User)


class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    add_form = CustomUserForm
    model = User
    list_display = ['email', 'username',]


admin.site.register(User, CustomUserAdmin)
