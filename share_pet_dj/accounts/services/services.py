"""
This module is used for working with
business logic in the app.
"""
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.forms import model_to_dict

from accounts.models import Setting
from core.exceptions import FormSaveError, AccountDoesNotExist
from notifications.models import Notification

Account = get_user_model()


class ProfileService:
    @staticmethod
    def _create_profile_settings(*args, **kwargs) -> None:
        setting = Setting.objects.create(*args, **kwargs)
        Notification.objects.create(setting=setting)

    @staticmethod
    def _get_setting(*args, **kwargs) -> Setting:
        return Setting.objects.get(*args, **kwargs)

    @staticmethod
    def _get_notification(*args, **kwargs) -> Notification:
        return Notification.objects.get(*args, **kwargs)

    @staticmethod
    def _update_avatar(account: Account, *args, **kwargs) -> None:
        account.avatar.save(*args, **kwargs)
        account.save()

    @staticmethod
    def _update_account(pk: int, *args, **kwargs) -> None:
        Account.objects.filter(pk=pk).update(*args, **kwargs)

    @staticmethod
    def _get_account(*args, **kwargs) -> Account:
        return Account.objects.get(*args, **kwargs)

    def create_profile_settings(self, *args, **kwargs) -> None:
        self._create_profile_settings(*args, **kwargs)

    def get_data(self, *args, **kwargs) -> dict:
        account = self._get_account(*args, **kwargs)
        setting = self._get_setting(account=account)
        notification = self._get_notification(setting=setting)

        account_dict = model_to_dict(account, fields=(
            'username', 'first_name',
            'last_name', 'email', 'avatar'
        ))

        setting_dict = model_to_dict(setting, fields=('language', 'status'))

        notification_dict = model_to_dict(notification, fields=(
            'signup', 'login', 'changing_profile',
            'changing_setting', 'sb_liked_comment',
            'sb_replied_to_comment', 'sb_liked_article',
            'new_comment', 'sb_liked_animal', 'new_message',
            'deal_start', 'deal_timeout', 'deal_finish', 'refill'
        ))

        return {
            'account': account_dict,
            'setting': setting_dict,
            'notification': notification_dict
        }

    def update_avatar(self, account: Account, *args, **kwargs) -> None:
        self._update_avatar(account, *args, **kwargs)

    def update_account(self, pk: int, *args, **kwargs) -> None:
        self._update_account(pk, *args, **kwargs)

    def get_account(self, *args, **kwargs) -> Account:
        try:
            return self._get_account(*args, **kwargs)
        except Account.DoesNotExist:
            raise AccountDoesNotExist


class ResetPasswordService:
    @staticmethod
    def _get_accounts_with_status_fields(*args, **kwargs) -> QuerySet[Account]:
        accounts = Account.objects.filter(*args, **kwargs)
        return accounts.values('is_administrator', 'is_superuser')

    def raise_exception_if_not_user(self, *args, **kwargs) -> None:
        accounts = self._get_accounts_with_status_fields(*args, **kwargs)

        for account in accounts:
            if account['is_administrator'] or account['is_superuser']:
                raise FormSaveError('You cannot reset your password.')
