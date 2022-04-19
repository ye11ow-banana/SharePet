from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.utils import build_absolute_uri

from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


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
            user.avatar.save(file.name, file, save=True)
            user.save()

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
        administrator.is_administrator = True
        administrator.save()

        return administrator


class ResetPasswordForm(AllauthResetPasswordForm):
    """Reset password form if user forget the password."""
    def clean(self):
        """Reset password can only user."""
        cleaned_data = super().clean()

        accounts = get_user_model().objects.filter(
            email=cleaned_data.get('email'))

        for account in accounts:
            if account.is_administrator or account.is_superuser:
                self.add_error(
                    'email', _('You cannot reset your password.'))

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
