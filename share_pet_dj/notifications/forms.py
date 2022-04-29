from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        fields = (
            'signup', 'login', 'changing_profile',
            'changing_setting', 'sb_liked_comment',
            'sb_replied_to_comment', 'sb_liked_article',
            'new_comment', 'sb_liked_animal', 'new_message',
            'deal_start', 'deal_timeout', 'deal_finish', 'refill'
        )
        model = Notification
