"""
This module is used for working
with data in the app.

For example, Django ORM or sessions.
"""
from typing import Generator, Type

from django.contrib.auth import get_user_model

from accounts.models import Setting
from accounts.services.dataclasses import AccountData
from core.repository import ModelObject

Account = get_user_model()


class AccountUpdate:
    """Logic for updating account model."""
    _model_object = ModelObject(Account)

    @staticmethod
    def update_avatar(account: Account, *args, **kwargs) -> None:
        account.avatar.save(*args, **kwargs)
        account.save()

    def update_fields_by_pk(self, pk: int, **kwargs) -> None:
        self._model_object.update_fields_by_pk(pk, **kwargs)


class AccountGet:
    """Logic for getting account model."""
    _model_object = ModelObject(Account)

    def get_account(self, fields: tuple, **kwargs) -> dict:
        return self._model_object.get_model_object(fields, **kwargs)

    def get_pure_account(self, *args, **kwargs) -> Account:
        return self._model_object.get_pure_model_object(*args, **kwargs)

    def get_all_with_fields(
            self, fields: tuple
    ) -> Generator[AccountData, None, None]:
        for model in self._model_object.get_all_with_fields(fields):
            yield model


class AccountRepository(AccountGet, AccountUpdate):
    """Logic for account model."""


class SettingUpdate:
    """Logic for updating `Setting` model."""
    _model_object = ModelObject(Setting)

    def update_fields_by_pk(self, pk: int, **kwargs) -> None:
        self._model_object.update_fields_by_pk(pk, **kwargs)


class SettingGet:
    """Logic for getting `Setting` model."""
    _model_object = ModelObject(Setting)

    def get_setting(self, fields: tuple, **kwargs) -> dict:
        return self._model_object.get_model_object(fields, **kwargs)


class SettingRepository(SettingGet, SettingUpdate):
    """Logic for `Setting` model."""
