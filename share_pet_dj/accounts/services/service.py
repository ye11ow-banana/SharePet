"""
This module is used for working with
business logic in the app.
"""
from dataclasses import dataclass
from typing import Iterator

from accounts.infrastructure import AccountData, SettingData
from core.exceptions import FormSaveError
from notifications.infrastructure import NotificationData


class ProfileSettings:
    @staticmethod
    def _create_profile_settings(*args, **kwargs) -> None:
        setting = SettingData().create(*args, **kwargs)
        NotificationData().create(setting=setting)

    def create_profile_settings(self, *args, **kwargs) -> None:
        self._create_profile_settings(*args, **kwargs)


@dataclass
class AccountResetPasswordRow:
    is_administrator: bool
    is_superuser: bool


class ResetPasswordService:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    @staticmethod
    def _get_accounts_with_status_fields(
            *args, **kwargs) -> Iterator[AccountResetPasswordRow]:
        account_data = AccountData()

        accounts = account_data.filter(*args, **kwargs)
        accounts_iter = account_data.values(
            accounts, 'is_administrator', 'is_superuser')

        for account in accounts_iter:
            yield AccountResetPasswordRow(
                is_administrator=account['is_administrator'],
                is_superuser=account['is_superuser']
            )

    def raise_exception_if_not_user(self) -> None:
        accounts_iter = self._get_accounts_with_status_fields(
            *self._args, **self._kwargs)

        for account in accounts_iter:
            if account.is_administrator or account.is_superuser:
                raise FormSaveError('You cannot reset your password.')
