from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .form import CustomUserForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserForm
    model = User
    list_display = ['email', 'username',]


admin.site.register(User, CustomUserAdmin)
