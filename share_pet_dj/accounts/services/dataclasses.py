from dataclasses import dataclass

from django.contrib.auth import get_user_model

from accounts.forms import AccountForm, SettingForm
from notifications.forms import NotificationForm


Account = get_user_model()


@dataclass(frozen=True)
class AccountFormProfileData:
    form_name: str
    account: Account
    form: AccountForm | SettingForm | NotificationForm = None
