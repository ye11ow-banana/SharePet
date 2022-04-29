from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Setting
from notifications.models import Notification

Account = get_user_model()


class NotificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create()

    def test_create(self):
        """Notification instance is created correctly."""
        setting = Setting.objects.create(account=self.account)
        notification = Notification.objects.create(
            setting=setting, refill=False)

        self.assertEquals(Notification.objects.count(), 1)
        self.assertEquals(notification.setting.account, self.account)
        self.assertTrue(notification.signup)
        self.assertTrue(notification.login)
        self.assertTrue(notification.changing_profile)
        self.assertTrue(notification.changing_setting)
        self.assertTrue(notification.sb_liked_comment)
        self.assertTrue(notification.sb_replied_to_comment)
        self.assertTrue(notification.sb_liked_article)
        self.assertTrue(notification.new_comment)
        self.assertTrue(notification.sb_liked_animal)
        self.assertTrue(notification.new_message)
        self.assertTrue(notification.deal_start)
        self.assertTrue(notification.deal_timeout)
        self.assertTrue(notification.deal_finish)
        self.assertFalse(notification.refill)

    def test_db_table_name(self):
        """
        Model instance must have db table
        with particular name.
        """
        setting = Setting.objects.create(account=self.account)
        notification = Notification.objects.create(setting=setting)
        self.assertEquals(notification._meta.db_table, 'notification')

    def test_ordering(self):
        """Model instances must be ordered by account date_joined."""
        setting1 = Setting.objects.create(account=self.account)
        Notification.objects.create(setting=setting1)
        account2 = Account.objects.create()
        setting2 = Setting.objects.create(account=account2)
        notification2 = Notification.objects.create(setting=setting2)

        last_notification = Notification.objects.last()

        self.assertEquals(last_notification, notification2)

        account3 = Account.objects.create(
            date_joined=self.account.date_joined)
        setting3 = Setting.objects.create(account=account3)
        Notification.objects.create(setting=setting3)

        last_notification = Notification.objects.last()

        self.assertEquals(last_notification, notification2)

    def test_conversion_to_string(self):
        """
        Model instance must be cast to a string type
        in the form of account username or email, whichever exists.
        """
        account1 = Account.objects.create(username='username1')
        account2 = Account.objects.create(email='email2')

        setting1 = Setting.objects.create(account=account1)
        setting2 = Setting.objects.create(account=account2)

        notification1 = Notification.objects.create(setting=setting1)
        notification2 = Notification.objects.create(setting=setting2)

        self.assertEquals(str(notification1), account1.username)
        self.assertEquals(str(notification2), account2.email)
