import shutil
import time

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from accounts.models import Account
from config.settings import MEDIA_ROOT

TEST_DIR = 'test_data'


class TestAccountModel(TestCase):
    """Test `Account` model."""
    def setUp(self):
        self.file_name = 'test'
        self.file_path = f'{MEDIA_ROOT}/tests/{self.file_name}.jpg'
        self.account = Account.objects.create()

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


def tearDownModule():
    """
    Delete TEST_DIR after test functions
    working with files.
    """
    try:
        shutil.rmtree(TEST_DIR)
    except OSError:
        pass
