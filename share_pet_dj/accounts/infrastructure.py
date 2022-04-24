"""
This module is used for working with datas.

For example, APIs, Django ORM, SQLAlchemy or another.
"""
from typing import Iterator

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from .models import Setting


class AccountData:
    """Work with `account` model."""
    _Account = get_user_model()

    @staticmethod
    def update_avatar(account: _Account, *args, **kwargs) -> None:
        account.avatar.save(*args, **kwargs)
        account.save()

    def update(self, pk: int, *args, **kwargs) -> None:
        self._Account.objects.filter(pk=pk).update(*args, **kwargs)

    def filter(self, *args, **kwargs) -> QuerySet:
        return self._Account.objects.filter(*args, **kwargs)

    @staticmethod
    def values(
            accounts: QuerySet[_Account],
            *args, **kwargs) -> Iterator[dict]:
        for account in accounts.values(*args, **kwargs):
            yield account

    # def all(self) -> QuerySet:
    #     return self._Account.objects.all()


class SettingData:
    @staticmethod
    def create(*args, **kwargs) -> Setting:
        return Setting.objects.create(*args, **kwargs)
