from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """Notifications of an account."""
    setting = models.OneToOneField(
        'accounts.Setting', on_delete=models.CASCADE,
        verbose_name=_('setting')
    )
    signup = models.BooleanField(_('signup'), default=True)
    login = models.BooleanField(_('login'), default=True)
    changing_profile = models.BooleanField(_('changing profile'), default=True)
    changing_setting = models.BooleanField(_('changing setting'), default=True)
    sb_liked_comment = models.BooleanField(
        _('somebody liked comment'), default=True)
    sb_replied_to_comment = models.BooleanField(
        _('somebody replied to comment'), default=True)
    sb_liked_article = models.BooleanField(
        _('somebody liked article'), default=True)
    new_comment = models.BooleanField(_('new comment'), default=True)
    sb_liked_animal = models.BooleanField(
        _('somebody liked animal'), default=True)
    new_message = models.BooleanField(_('new message'), default=True)
    deal_start = models.BooleanField(_('deal start'), default=True)
    deal_timeout = models.BooleanField(_('deal timeout'), default=True)
    deal_finish = models.BooleanField(_('deal finish'), default=True)
    refill = models.BooleanField(_('refill'), default=True)

    class Meta:
        db_table = 'notification'
        ordering = 'setting__account',
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')

    def __str__(self):
        return str(self.setting.account)
