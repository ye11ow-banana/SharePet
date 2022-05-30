from typing import Literal, Sequence

from django.forms import BaseForm


class FormUtil:
    @staticmethod
    def get_checked_form(form: BaseForm):
        if form.is_valid():
            pass

        return form

    @staticmethod
    def add_errors_to_form(
            form: BaseForm, errors: Sequence[
                dict[
                    Literal['field'] | Literal['error_messages'],
                    str | Sequence[str]
                ]
            ] | Sequence
    ) -> BaseForm:
        for error in errors:
            form.add_error(error['field'], error['error_messages'])

        return form
