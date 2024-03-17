from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'family_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'family_name', 'first_name', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'family_name', 'first_name', 'is_active', 'is_staff', 'is_superuser']

admin.site.register(CustomUser, CustomUserAdmin)
