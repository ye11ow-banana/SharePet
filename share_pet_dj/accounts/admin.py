from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Setting


Account = get_user_model()


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin class for an account"""


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Admin class for a setting"""
