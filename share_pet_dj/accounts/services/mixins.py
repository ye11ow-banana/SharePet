"""
This module is used for logic
that repeats in `views.py`.
"""
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
