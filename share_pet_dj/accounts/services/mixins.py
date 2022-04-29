from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from accounts.forms import AccountForm, SettingForm
from accounts.models import Setting
from accounts.services.dataclasses import AccountFormProfileData
from accounts.services.services import ProfileService
from notifications.forms import NotificationForm
from notifications.models import Notification

Account = get_user_model()


class ProfileMixin:
    @staticmethod
    def _get_profile_forms(*args, **kwargs) -> dict:
        fields_data = ProfileService().get_data(*args, **kwargs)

        return {
            'account_form': AccountForm(initial=fields_data['account']),
            'setting_form': SettingForm(initial=fields_data['setting']),
            'notification_form': NotificationForm(
                initial=fields_data['notification'])
        }

    @staticmethod
    def _get_instance_for_form(data_obj: AccountFormProfileData) -> (
        Account | Setting | Notification
    ):
        match data_obj.form_name:
            case 'account_form':
                return data_obj.account
            case 'setting_form':
                return get_object_or_404(Setting, account=data_obj.account)
            case _:
                return get_object_or_404(
                    Notification, setting__account=data_obj.account)

    def _update_context_if_form_valid(
            self, data_obj: AccountFormProfileData) -> dict:
        if data_obj.form.is_valid():
            context_update = {'success': True}
            data_obj.form.save()
        else:
            context_update = {
                'success': False,
                data_obj.form_name: data_obj.form
            }

        context = self._get_profile_forms(pk=data_obj.account.pk)
        context.update(context_update)

        return context

    def post(self, request):
        account = request.user

        forms = {
            'account_form': AccountForm,
            'setting_form': SettingForm,
            'notification_form': NotificationForm
        }

        form_name = request.POST['form-type']
        data_obj = AccountFormProfileData(form_name=form_name, account=account)
        instance = self._get_instance_for_form(data_obj)

        form = forms[form_name](request.POST, instance=instance)
        data_obj = AccountFormProfileData(
            form_name=form_name, account=account, form=form)
        context = self._update_context_if_form_valid(data_obj)

        return render(request, 'accounts/profile.html', context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        profile_forms = self._get_profile_forms(pk=self.request.user.pk)

        context.update(profile_forms)

        return context
