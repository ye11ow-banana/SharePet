"""
This module is used for changing default
django-allauth behaviour.
"""
from allauth.account.views import SignupView, sensitive_post_parameters_m
from allauth.exceptions import ImmediateHttpResponse

from django.views.generic import FormView

from core.exceptions import CreateInstanceError


class ContextDataMixin:
    """Change `get_context_data` function."""
    def __new__(cls, *args, **kwargs):
        if cls is ContextDataMixin:
            raise CreateInstanceError(__class__.__name__)
        return super().__new__(cls, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Delete django-allauth functionality of the method.
        For example, some reverse() methods because is used
        new namespacing for urls.
        """
        return FormView.get_context_data(self, **kwargs)


class AdministratorSignup(SignupView):
    """Custom signup logic for `administrator` user."""
    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        """
        Override the `dispatch` method deleting
        `RedirectAuthenticatedUserMixin` from inheriting tree.
        """
        try:
            if not self.is_open():
                return self.closed()
        except ImmediateHttpResponse as e:
            return e.response
        return FormView.dispatch(self, request, *args, **kwargs)
