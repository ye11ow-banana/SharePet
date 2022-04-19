from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from accounts.managers import AccountManager


class Account(AbstractUser):
    """
    Main user model.

    If user has is_administrator=True, user is administrator.
    If user has is_superuser=True, user is admin.
    Otherwise, just user.

    If unknown particular type of user, it is account.
    """
    username_validator = UnicodeUsernameValidator()

    avatar = ResizedImageField(upload_to='accounts/%Y/%m/%d',
                               blank=True, null=True)
    username = models.CharField(
        _('username'), max_length=150, unique=True, blank=True, null=True,
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        _('email address'), unique=True, blank=True, null=True
    )
    is_administrator = models.BooleanField(
        _('administrator status'),
        blank=True,
        default=False,
        help_text=_('Designates whether this user '
                    'should have more stuff rights.'),
    )
    date_baned = models.DateTimeField(_('date baned'), blank=True, null=True)

    objects = AccountManager()

    class Meta:
        db_table = 'account'
        ordering = 'date_joined',
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return self.username or self.email
