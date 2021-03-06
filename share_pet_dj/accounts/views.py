from allauth.account.views import (
    ConfirmEmailView as AllauthConfirmEmailView,
    LoginView as AllauthLoginView,
    PasswordChangeView as AllauthPasswordChangeView,
    PasswordResetFromKeyView as AllauthPasswordResetFromKeyView,
    PasswordResetView as AllauthPasswordResetView,
    SignupView as AllauthSignupView
)
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import ResetPasswordForm, SignupAdministratorForm, SignupUserForm
from core.decorators import account_allower
from .services.mixins import ContextDataMixin
from .services.services import ProfileService, AdministratorSignup


@method_decorator(transaction.atomic, name='dispatch')
class UserSignupView(ContextDataMixin, AllauthSignupView):
    """Registration view for regular user."""
    template_name = 'accounts/signup_user.html'
    form_class = SignupUserForm


@method_decorator(
    (account_allower(redirect_url=reverse_lazy('login'), allow_to='admin'),
     transaction.atomic), name='dispatch')
class AdministratorSignupView(ContextDataMixin, AdministratorSignup):
    """Registration view for administrator."""
    template_name = 'accounts/signup_administrator.html'
    form_class = SignupAdministratorForm


class EmailVerificationSentView(TemplateView):
    """
    Tell account that was sent
    email verification to the email.
    """
    template_name = 'accounts/confirm_email_sent.html'


class ConfirmEmailView(AllauthConfirmEmailView):
    """Confirm account registration and email."""
    template_name = 'accounts/confirm_email.html'

    def post(self, *args, **kwargs):
        super().post()
        return redirect(reverse_lazy('login'))


class LoginView(ContextDataMixin, AllauthLoginView):
    """Login view."""
    template_name = 'accounts/login.html'


@method_decorator(
    account_allower(redirect_url=reverse_lazy('profile'),
                    allow_to='anonymous'), name='dispatch')
class PasswordResetView(ContextDataMixin, AllauthPasswordResetView):
    """Page with email input if user forget a password."""
    template_name = 'accounts/password_reset.html'
    form_class = ResetPasswordForm


@method_decorator(
    account_allower(redirect_url=reverse_lazy('profile'),
                    allow_to='anonymous'), name='dispatch')
class PasswordResetDoneView(TemplateView):
    """
    Page tells user that letter has been sent to email
    for changing user password.
    """
    template_name = 'accounts/password_reset_done.html'


@method_decorator(
    account_allower(redirect_url=reverse_lazy('profile'),
                    allow_to='anonymous'), name='dispatch')
class PasswordResetFromKeyView(AllauthPasswordResetFromKeyView):
    """Page for entering new password."""
    template_name = 'accounts/password_reset_from_key.html'


@method_decorator(
    account_allower(redirect_url=reverse_lazy('profile'),
                    allow_to='anonymous'), name='dispatch')
class PasswordResetFromKeyDoneView(TemplateView):
    """Password has been changed successfully page."""
    template_name = 'accounts/password_reset_from_key_done.html'


@method_decorator(
    account_allower(redirect_url=reverse_lazy('profile'), allow_to='user'),
    name='dispatch')
class PasswordChangeView(AllauthPasswordChangeView):
    """Page for changing password."""
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    _profile_service = ProfileService()
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_forms = self._profile_service.get_profile_forms(
            pk=self.request.user.pk)
        context.update(profile_forms)

        return context

    def post(self, request):
        data = request.POST.dict()
        form_name = data['form-type']
        del data['csrfmiddlewaretoken']
        del data['form-type']

        context = self._profile_service.execute(
            pk=request.user.pk,
            form_name=form_name,
            data_to_update=data
        )

        return render(request, 'accounts/profile.html', context)


signup_user = UserSignupView.as_view()
signup_administrator = AdministratorSignupView.as_view()
email_verification_sent = EmailVerificationSentView.as_view()
confirm_email = ConfirmEmailView.as_view()
login = LoginView.as_view()
logout = require_POST(LogoutView.as_view())
password_reset = PasswordResetView.as_view()
password_reset_done = PasswordResetDoneView.as_view()
password_reset_from_key = PasswordResetFromKeyView.as_view()
password_reset_from_key_done = PasswordResetFromKeyDoneView.as_view()
change_password = PasswordChangeView.as_view()
profile = ProfileView.as_view()
