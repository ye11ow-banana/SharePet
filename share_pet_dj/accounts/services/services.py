"""
This module is used for working with
application logic in the app.

Repository + domain logic.
"""
from typing import Callable

from django.contrib.auth import get_user_model
from django.forms import BaseForm

from core.utils import FormUtil
from notifications.forms import NotificationForm
from notifications.services.repository import NotificationRepository
from .domain import AccountDomain
from .repository import AccountRepository, SettingRepository
from accounts.forms import AccountForm, SettingForm

Account = get_user_model()


class ProfileUpdate:
    """Logic for updating account profile."""
    _account_repository = AccountRepository()
    _setting_repository = SettingRepository()

    @staticmethod
    def _update(
            pk: int, data_to_update: dict,
            update_method: Callable
    ) -> None:
        update_method(pk, **data_to_update)


class ProfileGet:
    """Logic for getting account profile."""
    _account_repository = AccountRepository()
    _setting_repository = SettingRepository()
    _notification_repository = NotificationRepository()

    def _get_pk_by_form_name(self, pk: int, form_name: str) -> int:
        if 'setting' in form_name:
            pk = self._setting_repository.get_setting(
                fields=('id',), account_id=pk).get('id')
        elif 'notification' in form_name:
            pk = self._notification_repository.get_notification(
                fields=('id',), setting__account_id=pk).get('id')

        return pk

    def _get_form_and_update_method(self, form_name: str) -> tuple:
        forms_and_update_methods = {
            'account_form': (
                AccountForm, self._account_repository.update_fields_by_pk
            ),
            'setting_form': (
                SettingForm, self._setting_repository.update_fields_by_pk
            ),
            'notification_form': (
                NotificationForm,
                self._notification_repository.update_fields_by_pk
            ),
        }

        try:
            result = forms_and_update_methods[form_name]
        except KeyError:
            raise KeyError('Form name has been changed.')
        else:
            return result

    def _get_profile_data(self, pk: int) -> dict:
        account_dict = self._account_repository.get_account(fields=(
            'username', 'first_name',
            'last_name', 'email', 'avatar'
        ), id=pk)

        setting_dict = self._setting_repository.get_setting(fields=(
            'language', 'status'
        ), account_id=pk)

        notification_dict = self._notification_repository.get_notification(
            fields=(
                'signup', 'login',
                'changing_profile',
                'changing_setting',
                'sb_liked_comment',
                'sb_replied_to_comment',
                'sb_liked_article',
                'new_comment', 'sb_liked_animal',
                'new_message',
                'deal_start', 'deal_timeout',
                'deal_finish', 'refill'
            ), setting__account_id=pk)

        return {
            'account': account_dict,
            'setting': setting_dict,
            'notification': notification_dict
        }

    def get_profile_forms(self, pk: int) -> dict:
        fields_data = self._get_profile_data(pk)

        return {
            'account_form': AccountForm(initial=fields_data['account']),
            'setting_form': SettingForm(initial=fields_data['setting']),
            'notification_form': NotificationForm(
                initial=fields_data['notification'])
        }


class ProfileService(ProfileGet, ProfileUpdate):
    """Logic for account profile."""
    _form_util = FormUtil()
    _account_domain = AccountDomain()

    @staticmethod
    def _is_email_changed(email: str, account: dict) -> bool:
        if email == account.get('email'):
            return False

        return True

    def _get_valid_data_errors(
            self, pk: int, data_to_update: dict
    ) -> list[dict[str, str]]:
        username = data_to_update.get('username')
        email = data_to_update.get('email')
        errors = []

        if username is None or email is None:
            return errors

        accounts = self._account_repository.get_all_with_fields(
            fields=('id', 'username'))
        account = self._account_repository.get_account(
            fields=('email',), pk=pk)

        errors.extend(self._account_domain.is_username_valid(
            pk, username, accounts)
        )
        if self._is_email_changed(email, account):
            errors.append({
                'field': 'email',
                'error_messages': ['You cannot change email right here!']
            })

        return errors

    def _is_valid(
            self, pk: int, form_class,
            data_to_update: dict
    ) -> tuple[bool, BaseForm]:
        result = True

        form = form_class(data_to_update)
        form = self._form_util.get_checked_form(form)
        errors = self._get_valid_data_errors(pk, data_to_update)

        if form.errors or errors:
            result = False

        if errors:
            form = self._form_util.add_errors_to_form(form, errors)

        return result, form

    def _create_response_context(
            self, pk: int, result: bool,
            form: BaseForm, form_name: str
    ) -> dict:
        response_context = {'success': True}
        response_context.update(self.get_profile_forms(pk))

        if not result:
            response_context.update({'success': False})
            response_context.get(form_name)._errors = form.errors

        return response_context

    def execute(self, pk: int, form_name: str, data_to_update: dict) -> dict:
        form_class, update_method = self._get_form_and_update_method(form_name)
        result, form = self._is_valid(pk, form_class, data_to_update)

        if result:
            pk_to_update = self._get_pk_by_form_name(pk, form_name)
            self._update(pk_to_update, data_to_update, update_method)

        return self._create_response_context(pk, result, form, form_name)
