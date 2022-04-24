from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.utils import build_absolute_uri

from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from core.exceptions import FormSaveError
from .infrastructure import AccountData
from .services.service import ResetPasswordService, ProfileSettings


class SignupUserForm(AllauthSignupForm, forms.ModelForm):
    """Registration form for regular user."""
    class Meta:
        model = get_user_model()
        fields = (
            'avatar', 'first_name', 'last_name',
            'username', 'email',
        )

    def save(self, request):
        user = super().save(request)
        file = self.cleaned_data['avatar']

        if file is not None:
            AccountData().update_avatar(user, file.name, file, save=True)

        ProfileSettings().create_profile_settings(account=user)

        return user


class SignupAdministratorForm(AllauthSignupForm, forms.ModelForm):
    """Registration form for administrator."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        del self.fields['username']

    class Meta:
        model = get_user_model()
        fields = 'first_name', 'last_name', 'email'

    def save(self, request):
        administrator = super().save(request)
        AccountData().update(administrator.pk, is_administrator=True)
        ProfileSettings().create_profile_settings(account=administrator)

        return administrator


class ResetPasswordForm(AllauthResetPasswordForm):
    """Reset password form if user forget the password."""
    def clean(self):
        """Reset password can only user."""
        cleaned_data = super().clean()
        reset_password_service = ResetPasswordService(
            email=cleaned_data.get('email'))

        try:
            reset_password_service.raise_exception_if_not_user()
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
