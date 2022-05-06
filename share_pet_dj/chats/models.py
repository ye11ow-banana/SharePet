from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from config.settings import AUTH_USER_MODEL as Account


class Chat(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    accounts = models.ManyToManyField(Account, verbose_name=_('accounts'))
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    class Meta:
        db_table = 'chat'
        ordering = 'date_created',
        verbose_name = _('chat')
        verbose_name_plural = _('chats')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('chat_detail', kwargs={'chat_name': self.slug})


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    text = models.TextField(_('text'), blank=True, null=True)
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE,
        verbose_name=_('chat')
    )
    file = models.FileField(
        _('file'), upload_to='chats/%Y/%m/%d', blank=True, null=True)
    date_sent = models.DateTimeField(_('date sent'), default=timezone.now)

    class Meta:
        db_table = 'message'
        ordering = 'date_sent',
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return f'{self.date_sent} - {str(self.chat)}'
