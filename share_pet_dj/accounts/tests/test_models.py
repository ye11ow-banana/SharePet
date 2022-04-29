import shutil
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from accounts.models import Account, Setting
from config.settings import MEDIA_ROOT


TEST_DIR = 'test_data'


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = Account.objects.create()
        cls.file_name = 'test'

    def setUp(self):
        self.file_path = f'{MEDIA_ROOT}/tests/{self.file_name}.jpg'

    def tearDown(self):
        """
        Delete TEST_DIR after test functions
        working with files.
        """
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_image_upload_path(self):
        """Image of user avatar saves in correct place."""
        self.account.avatar = SimpleUploadedFile(
            name=f'{self.file_name}.jpeg',
            content=open(self.file_path, 'rb').read(),
            content_type='image/jpeg'
        )
        self.account.save()

        localtime = time.localtime(time.time())
        date_path = time.strftime('%Y/%m/%d', localtime)
        self.assertEquals(self.account.avatar.url,
                          f'/media/accounts/{date_path}/{self.file_name}.jpeg')

    def test_db_table_name(self):
        """
        Model instance must have db table
        with particular name.
        """
        self.assertEquals(self.account._meta.db_table, 'account')

    def test_ordering(self):
        """Model instances must be ordered by date_joined."""
        Account.objects.create()
        account2 = Account.objects.create()
        last_account = Account.objects.last()

        self.assertEquals(last_account, account2)

        account3 = Account.objects.create()
        Account.objects.create(date_joined=account2.date_joined)
        last_account = Account.objects.last()

        self.assertEquals(last_account, account3)

    def test_conversion_to_string(self):
        """
        Model instance must be cast to a string type
        in the form of its username or email, whichever exists.
        """
        account1 = Account.objects.create(username='username1')
        account2 = Account.objects.create(email='email2')

        self.assertEquals(str(account1), account1.username)
        self.assertEquals(str(account2), account2.email)


class SettingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Account = Account
        cls.account = Account.objects.create()

    def test_create(self):
        """Setting instance is created correctly."""
        setting = Setting.objects.create(account=self.account)

        self.assertEquals(Setting.objects.count(), 1)
        self.assertEquals(setting.account, self.account)
        self.assertEquals(setting.language, 'en')
        self.assertEquals(setting.status, 'alone_is_fine')

    def test_db_table_name(self):
        """
        Model instance must have db table
        with particular name.
        """
        setting = Setting.objects.create(account=self.account)
        self.assertEquals(setting._meta.db_table, 'setting')

    def test_ordering(self):
        """Model instances must be ordered by account date_joined."""
        Setting.objects.create(account=self.account)
        account2 = self.Account.objects.create()
        setting2 = Setting.objects.create(account=account2)

        last_setting = Setting.objects.last()

        self.assertEquals(last_setting, setting2)

        account3 = self.Account.objects.create(
            date_joined=self.account.date_joined)
        Setting.objects.create(account=account3)

        last_setting = Setting.objects.last()

        self.assertEquals(last_setting, setting2)

    def test_conversion_to_string(self):
        """
        Model instance must be cast to a string type
        in the form of account username or email, whichever exists.
        """
        account1 = self.Account.objects.create(username='username1')
        account2 = self.Account.objects.create(email='email2')

        setting1 = Setting.objects.create(account=account1)
        setting2 = Setting.objects.create(account=account2)

        self.assertEquals(str(setting1), account1.username)
        self.assertEquals(str(setting2), account2.email)
