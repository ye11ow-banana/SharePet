from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm as AllauthResetPasswordForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.utils import build_absolute_uri
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .services.repository import AccountRepository


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
        account_repository = AccountRepository()

        if file is not None:
            account_repository.update_avatar(user, file.name, file, save=True)

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
        account_repository = AccountRepository()

        account_repository.update_fields_by_pk(
            administrator.pk, is_administrator=True)

        return administrator


class ResetPasswordForm(AllauthResetPasswordForm):
    """Reset password form if user forget the password."""
    def clean(self):
        """Reset password can only user."""
        cleaned_data = super().clean()
        account_repository = AccountRepository()

        try:
            account = account_repository.get_pure_account(
                email=cleaned_data.get('email')
            )
        except Account.DoesNotExist:
            pass
        else:
            if account.is_administrator or account.is_staff:
                self.add_error('email', _('You cannot reset your password.'))

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


class AccountForm(forms.Form):
    username_validator = UnicodeUsernameValidator()

    username = forms.CharField(
        label=_('Username'),
        max_length=150,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
    )
    email = forms.EmailField(
        label=_('Email address'),
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    first_name = forms.CharField(label=_('First name'), max_length=150)
    last_name = forms.CharField(label=_('Last name'), max_length=150)
    avatar = forms.ImageField(label=_('Avatar'), required=False)


class SettingForm(forms.Form):
    LANGUAGES = (
        ('ua', _('Ukrainian')),
        ('en', _('English')),
        ('ru', _('Russian'))
    )
    STATUS = (
        ('actively_looking', _('actively looking')),
        ('alone_is_fine', _('alone is fine'))
    )

    language = forms.ChoiceField(
        label=_('Language'), choices=LANGUAGES,
        widget=forms.Select()
    )
    status = forms.ChoiceField(
        label=_('Status'), choices=STATUS,
        widget=forms.Select()
    )
