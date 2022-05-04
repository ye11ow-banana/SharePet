from django import forms

from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        fields = 'text', 'file'
        model = Message
