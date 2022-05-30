"""
This module is used for working with
domain logic in the app.
"""
from typing import Generator, Sequence

from config.settings import ACCOUNT_USERNAME_BLACKLIST
from .data_structures import AccountData


class AccountDomain:
    @staticmethod
    def is_username_valid(
            pk: int, username: str,
            accounts: Generator[AccountData, None, None]
    ) -> list[dict[str, Sequence[str]]]:
        errors = []

        for account in accounts:
            if account.pk == pk:
                continue

            if account.username == username:
                errors.append({
                    'field': 'username',
                    'error_messages': ['A user with that username '
                                       'already exists.']
                })
                break

            if username in ACCOUNT_USERNAME_BLACKLIST:
                errors.append({
                    'field': 'username',
                    'error_messages': ['Username can not be used. '
                                       'Please use other username.']
                })
                break

        return errors
