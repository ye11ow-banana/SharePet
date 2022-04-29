from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import (
    SignupUserForm, SignupAdministratorForm,
    ResetPasswordForm
)
from config.settings import MEDIA_ROOT

Account = get_user_model()


class SignupUserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.file_name = 'test'

    def setUp(self):
        self.file_path = f'{MEDIA_ROOT}/tests/{self.file_name}.jpg'

    def test_valid_data(self):
        """Test form working with correct full data."""
        with open(self.file_path, 'rb') as f:
            form = SignupUserForm(data={
                'username': 'username',
                'email': 'email@gmail.com',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'password1': 'password_',
                'password2': 'password_',
                'avatar': f,
            })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        """Test form working without data. Check errors."""
        form = SignupUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
        self.assertEquals(form.errors['username'], ['This field is required.'])
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['password1'],
                          ['This field is required.'])
        self.assertEquals(form.errors['password2'],
                          ['This field is required.'])

    def test_invalid_data(self):
        """Test form working with invalid data. Check errors."""
        form = SignupUserForm(data={
            'username': '|||',
            'email': 'email',
            'password1': 'email',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
        self.assertEquals(
            form.errors['username'],
            ['Enter a valid username. This value may contain only letters,'
             ' numbers, and @/./+/-/_ characters.']
        )
        self.assertEquals(form.errors['email'],
                          ['Enter a valid email address.'])
        self.assertEquals(
            form.errors['password1'],
            [
                'This password is too short. '
                'It must contain at least 8 characters.',
                'This password is too common.',
            ]
        )
        self.assertEquals(form.errors['password2'],
                          ['This field is required.'])


class ResetPasswordFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrator = Account.objects.create(
            email='administrator@gmail.com', is_administrator=True)

    def test_valid_data(self):
        """Test form working with correct full data."""
        form = ResetPasswordForm(data={'email': 'email@gmail.com'})

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        """Test form working without data. Check errors."""
        form = ResetPasswordForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'], ['This field is required.'])

    def test_invalid_data(self):
        """Test form working with invalid data. Check errors."""
        form = ResetPasswordForm(data={'email': 'email'})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'],
                          ['Enter a valid email address.'])

    def test_clean_non_user_email(self):
        """Test `clean` function with non-user email."""
        form = ResetPasswordForm(data={'email': self.administrator.email})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEquals(form.errors['email'],
                          ['You cannot reset your password.'])


class SignupAdministratorFormTest(TestCase):
    def test_valid_data(self):
        """Test form working with correct full data."""
        form = SignupAdministratorForm(data={
                'email': 'email@gmail.com',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'password1': 'password_',
                'password2': 'password_',
            })

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        """Test form working without data. Check errors."""
        form = SignupAdministratorForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
        self.assertEquals(form.errors['email'], ['This field is required.'])
        self.assertEquals(form.errors['first_name'],
                          ['This field is required.'])
        self.assertEquals(form.errors['last_name'],
                          ['This field is required.'])
        self.assertEquals(form.errors['password1'],
                          ['This field is required.'])
        self.assertEquals(form.errors['password2'],
                          ['This field is required.'])

    def test_invalid_data(self):
        """Test form working with invalid data. Check errors."""
        form = SignupAdministratorForm(data={
            'username': '|||',
            'email': 'email',
            'password1': 'email',
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)
        self.assertEquals(form.errors['email'],
                          ['Enter a valid email address.'])
        self.assertEquals(form.errors['first_name'],
                          ['This field is required.'])
        self.assertEquals(form.errors['last_name'],
                          ['This field is required.'])
        self.assertEquals(
            form.errors['password1'],
            [
                'This password is too short. '
                'It must contain at least 8 characters.',
                'This password is too common.',
            ]
        )
        self.assertEquals(form.errors['password2'],
                          ['This field is required.'])
