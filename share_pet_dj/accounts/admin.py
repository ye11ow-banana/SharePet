from django.contrib import admin
from django.contrib.auth import get_user_model

Account = get_user_model()


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Admin class for account"""
