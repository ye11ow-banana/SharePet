from django import forms
from django.utils.translation import gettext_lazy as _


class NotificationForm(forms.Form):
    signup = forms.TypedChoiceField(
        label=_('Signup'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    login = forms.TypedChoiceField(
        label=_('Login'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    changing_profile = forms.TypedChoiceField(
        label=_('Changing profile'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    changing_setting = forms.TypedChoiceField(
        label=_('Changing setting'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    sb_liked_comment = forms.TypedChoiceField(
        label=_('Somebody liked comment'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    sb_replied_to_comment = forms.TypedChoiceField(
        label=_('Somebody replied to comment'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    sb_liked_article = forms.TypedChoiceField(
        label=_('Somebody liked article'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    new_comment = forms.TypedChoiceField(
        label=_('New comment'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    sb_liked_animal = forms.TypedChoiceField(
        label=_('Somebody liked animal'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    new_message = forms.TypedChoiceField(
        label=_('New message'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    deal_start = forms.TypedChoiceField(
        label=_('Deal start'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    deal_timeout = forms.TypedChoiceField(
        label=_('Deal timeout'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    deal_finish = forms.TypedChoiceField(
        label=_('Deal finish'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
    refill = forms.TypedChoiceField(
        label=_('refill'),
        coerce=lambda x: x == 'True',
        choices=((False, 'Notice me'), (True, 'Please, no')),
        widget=forms.RadioSelect
    )
