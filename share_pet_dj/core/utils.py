from django.forms import BaseForm


class FormUtil:
    @staticmethod
    def get_checked_form(form: BaseForm):
        if form.is_valid():
            pass

        return form

    @staticmethod
    def add_errors_to_form(
            form: BaseForm, errors: list[dict[str, str]]
    ) -> BaseForm:
        for error in errors:
            form.add_error(error['field'], error['error_messages'])

        return form
