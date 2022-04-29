from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.utils import build_absolute_uri

from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from core.exceptions import FormSaveError, AccountDoesNotExist
from .models import Setting
from .services import services

Account = get_user_model()


class SignupUserForm(AllauthSignupForm, forms.ModelForm):
    """Registration form for regular user."""
    class Meta:
        model = Account
        fields = (
            'avatar', 'first_name', 'last_name',
            'username', 'email',
        )

    def save(self, request):
        user = super().save(request)
        file = self.cleaned_data['avatar']
        profile_service = services.ProfileService()

        if file is not None:
            profile_service.update_avatar(user, file.name, file, save=True)

        profile_service.create_profile_settings(account=user)

        return user


class SignupAdministratorForm(AllauthSignupForm, forms.ModelForm):
    """Registration form for administrator."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        del self.fields['username']

    class Meta:
        model = Account
        fields = 'first_name', 'last_name', 'email'

    def save(self, request):
        administrator = super().save(request)
        profile_service = services.ProfileService()

        profile_service.update_account(
            administrator.pk, is_administrator=True)
        profile_service.create_profile_settings(account=administrator)

        return administrator


class ResetPasswordForm(AllauthResetPasswordForm):
    """Reset password form if user forget the password."""
    def clean(self):
        """Reset password can only user."""
        cleaned_data = super().clean()
        reset_password_service = services.ResetPasswordService()

        try:
            reset_password_service.raise_exception_if_not_user(
                email=cleaned_data.get('email')
            )
        except FormSaveError as e:
            self.add_error('email', _(str(e)))

        return cleaned_data

    def _send_unknown_account_mail(self, request, email: str) -> None:
        signup_url = build_absolute_uri(request, reverse('user_signup'))
        context = {
            'current_site': get_current_site(request),
            'email': email,
            'request': request,
            'signup_url': signup_url,
        }
        get_adapter(request).send_mail(
            'account/email/unknown_account', email, context)


class AccountForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        profile_service = services.ProfileService()

        try:
            profile_service.get_account(email=cleaned_data['email'])
        except AccountDoesNotExist:
            self.add_error('email', _('You cannot change email right here!'))

        return cleaned_data

    class Meta:
        fields = (
            'username', 'first_name',
            'last_name', 'email', 'avatar',
        )
        model = Account


class SettingForm(forms.ModelForm):
    class Meta:
        fields = 'language', 'status'
        model = Setting
