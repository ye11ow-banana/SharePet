import shutil
import time

from allauth.account.forms import (
    EmailAwarePasswordResetTokenGenerator, LoginForm)
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.account.utils import user_pk_to_url_str

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from accounts.forms import SignupAdministratorForm, SignupUserForm
from config.settings import MEDIA_ROOT

TEST_DIR = 'test_data'


class SignupUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Account = Account = get_user_model()

        cls.account = account = Account.objects.create(username='username1')
        account.set_password('password_')
        account.save()

        cls.url = reverse('user_signup')
        cls.file_name = 'test'

    def setUp(self):
        self.client = Client()
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

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), SignupUserForm)
        self.assertTemplateUsed(response, 'accounts/signup_user.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_POST(self):
        """
        Anonymous account sends POST request
        with correct full data.
        """
        with open(self.file_path, 'rb') as f:
            data = {
                'username': 'username2',
                'email': 'email2@gmail.com',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'password1': 'password_',
                'password2': 'password_',
                'avatar': f,
            }

            response = self.client.post(self.url, data=data)

        self.assertRedirects(
            response, reverse('account_email_verification_sent'), 302)
        self.assertEquals(self.Account.objects.count(), 2)

        account = self.Account.objects.last()
        self.assertFalse(account.is_administrator)
        self.assertEquals(account.username, data['username'])
        self.assertEquals(account.email, data['email'])
        self.assertEquals(account.first_name, data['first_name'])
        self.assertEquals(account.last_name, data['last_name'])
        self.assertTrue(account.check_password(data['password1']))

        localtime = time.localtime(time.time())
        date_path = time.strftime('%Y/%m/%d', localtime)
        self.assertEquals(account.avatar.url,
                          f'/media/accounts/{date_path}/{self.file_name}.jpeg')

    def test_POST_no_data(self):
        """Anonymous account sends POST request without data."""
        response = self.client.post(self.url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 4)
        self.assertFormError(response, 'form', 'username',
                             'This field is required.')
        self.assertFormError(response, 'form', 'email',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')

    def test_POST_invalid_data(self):
        """Anonymous account sends POST request with incorrect data."""
        response = self.client.post(
            self.url,
            data={
                'username': 'ye11ow_banana',  # forbidden username
                'email': 'email',
                'password1': 'email',
            },
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 4)
        self.assertFormError(
            response, 'form', 'username',
            'Username can not be used. Please use other username.'
        )
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')
        self.assertFormError(
            response, 'form', 'password1',
            [
                'This password is too short. '
                'It must contain at least 8 characters.',
                'This password is too common.',
            ]
        )
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')
        self.assertEquals(self.Account.objects.count(), 1)

    def test_authenticated_POST(self):
        """
        Authenticated account sends POST
        request with correct data.
        """
        data = {
            'username': 'username2',
            'email': 'email2@gmail.com',
            'password1': 'password_',
            'password2': 'password_',
        }

        self.client.login(username=self.account.username, password='password_')

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)
        self.assertEquals(self.Account.objects.count(), 1)


class PasswordResetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Account = Account = get_user_model()

        cls.user = user = Account.objects.create(
            username='username1', email='email1@gmail.com')
        user.set_password('password_')
        user.save()

        cls.url = reverse('password_reset')

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_authenticated_GET(self):
        """Authenticated user sends GET request."""
        self.client.login(username=self.user.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_POST(self):
        """Anonymous account sends POST request."""
        data = {'email': self.user.email}
        response = self.client.post(self.url, data=data)

        self.assertRedirects(
            response, reverse('account_reset_password_done'), 302)

    def test_POST_no_data(self):
        """Anonymous account sends POST request without data."""
        response = self.client.post(self.url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')
        self.assertEquals(len(response.context['form'].errors), 1)
        self.assertFormError(response, 'form', 'email',
                             'This field is required.')

    def test_POST_not_existing(self):
        """
        Anonymous account sends POST request
        with not existing user email.
        """
        data = {'email': 'not_existing_email@gmail.com'}
        response = self.client.post(self.url, data=data)

        self.assertRedirects(
            response, reverse('account_reset_password_done'), 302)

    def test_POST_non_user(self):
        """
        Anonymous account sends POST
        request with non-user email.
        """
        account = self.Account.objects.create(email='email2@gmail.com',
                                              is_administrator=True)
        account.set_password('password_')
        account.save()

        data = {'email': 'email2@gmail.com'}
        response = self.client.post(self.url, data=data)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')
        self.assertEquals(len(response.context['form'].errors), 1)
        self.assertFormError(response, 'form', 'email',
                             'You cannot reset your password.')

    def test_authenticated_POST(self):
        """Authenticated user sends POST request."""
        self.client.login(username=self.user.username, password='password_')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('profile'), 302)


class PasswordResetDoneViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('account_reset_password_done')

        cls.account = account = get_user_model().objects.create(username='username1')
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_POST(self):
        """Anonymous account sends POST request."""
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('profile'), 302)


class PasswordResetFromKeyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = account = get_user_model().objects.create(
            email='email@gmail.com')
        account.set_password('password_')
        account.save()

    @override_settings(ACCOUNT_RATE_LIMITS={'reset_password_email': '6/m'})
    def setUp(self):
        self.client = Client()

        self.client.post(reverse('password_reset'),
                         {'email': self.account.email})

        token_generator = EmailAwarePasswordResetTokenGenerator()
        temp_key = token_generator.make_token(self.account)

        self.uidb36 = user_pk_to_url_str(self.account)

        self.url = reverse(
            'account_reset_password_from_key',
            kwargs=dict(uidb36=self.uidb36, key=temp_key),
        )

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertRedirects(
            response, reverse(
                'account_reset_password_from_key',
                kwargs={'uidb36': self.uidb36, 'key': 'set-password'}
            ), 302)

        response = self.client.get(self.url, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'accounts/password_reset_from_key.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(email=self.account.email, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_POST(self):
        """Anonymous account sends POST request."""
        data = {
            'password1': 'password_',
            'password2': 'password_'
        }

        response = self.client.get(self.url)
        response = self.client.post(response.url, data=data)

        self.assertRedirects(
            response, reverse('account_reset_password_from_key_done'), 302)

    def test_POST_no_data(self):
        """Anonymous account sends POST request."""
        response = self.client.get(self.url)
        response = self.client.post(response.url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 2)
        self.assertFormError(response, 'form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')

    def test_POST_incorrect_password(self):
        """
        Anonymous account sends POST request
        with incorrect password.
        """
        data = {
            'password1': 'password',
            'password2': 'password'
        }

        response = self.client.get(self.url)
        response = self.client.post(response.url, data=data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 1)
        self.assertFormError(response, 'form', 'password1',
                             'This password is too common.')

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        data = {
            'password1': 'password_',
            'password2': 'password_'
        }

        self.client.login(email=self.account.email, password='password_')

        response = self.client.post(reverse('account_reset_password_from_key',
                                            kwargs={'uidb36': self.uidb36,
                                                    'key': 'set-password'}
                                            ), data=data)

        self.assertRedirects(response, reverse('profile'), 302)


class PasswordResetFromKeyDoneViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('account_reset_password_from_key_done')

        cls.account = account = get_user_model().objects.create(username='username1')
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'accounts/password_reset_from_key_done.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_POST(self):
        """Anonymous account sends POST request."""
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('profile'), 302)


class PasswordChangeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Account = Account = get_user_model()
        cls.url = reverse('password_change')

        cls.user = user = Account.objects.create(username='username1')
        user.set_password('password_')
        user.save()

        cls.account = account = Account.objects.create(
            username='username2', is_administrator=True)
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_authenticated_as_user_GET(self):
        """Authenticated user sends GET request."""
        self.client.login(username=self.user.username, password='password_')
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_authenticated_as_not_user_GET(self):
        """Authenticated non-user account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_POST(self):
        """Anonymous account sends POST request."""
        data = {
            'oldpassword': 'password_',
            'password1': '_password_',
            'password2': '_password_',
        }

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)

    def test_authenticated_as_user_POST(self):
        """Authenticated user sends POST request."""
        data = {
            'oldpassword': 'password_',
            'password1': '_password_',
            'password2': '_password_',
        }

        self.client.login(username=self.user.username, password='password_')
        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)
        self.assertTrue(
            self.Account.objects.get(
                pk=self.user.pk).check_password('_password_')
        )

    def test_authenticated_as_not_user_POST(self):
        """Authenticated non-user account sends POST request."""
        data = {
            'oldpassword': 'password_',
            'password1': '_password_',
            'password2': '_password_',
        }

        self.client.login(username=self.account.username, password='password_')

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)
        self.assertFalse(self.user.check_password('_password_'))

    def test_authenticated_as_user_POST_invalid_data(self):
        """
        Authenticated user sends POST
        request with invalid data.
        """
        data = {
            'oldpassword': 'password',
            'password1': 'password_',
            'password2': 'password__',
        }

        self.client.login(username=self.user.username, password='password_')

        response = self.client.post(self.url, data=data)
        self.assertEquals(len(response.context['form'].errors), 2)
        self.assertFormError(response, 'form', 'oldpassword',
                             'Please type your current password.')
        self.assertFormError(response, 'form', 'password2',
                             'You must type the same password each time.')


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('login')

        cls.account = account = get_user_model().objects.create(
            username='username1', email='email1')
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), LoginForm)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('profile'), 302)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=None)
    def test_username_POST(self):
        """
        Anonymous account sends POST request with correct data.
        Login with username.
        """
        data = {
            'login': self.account.username,
            'password': 'password_',
        }

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)
        self.assertIn('_auth_user_id', self.client.session)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION=None)
    def test_email_POST(self):
        """Anonymous account sends POST request with correct data.
        Login with email.
        """
        data = {
            'login': self.account.email,
            'password': 'password_',
        }

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('profile'), 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_POST_unverified(self):
        """
        Anonymous account sends POST request with
        correct data but with unverified email.
        """
        data = {
            'login': self.account.username,
            'password': 'password_',
        }

        response = self.client.post(self.url, data=data)

        self.assertRedirects(
            response,
            reverse('account_email_verification_sent'),
            302
        )
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_POST_no_data(self):
        """Anonymous account sends POST request without data."""
        response = self.client.post(self.url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(len(response.context['form'].errors), 2)
        self.assertFormError(response, 'form', 'login',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password',
                             'This field is required.')

    def test_POST_not_existing(self):
        """
        Anonymous account sends POST request with
        not existing account login.
        """
        data = {
            'login': 'not_existing_login',
            'password': 'password_'
        }

        response = self.client.post(self.url, data=data)

        self.assertEquals(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(len(response.context['form'].errors), 1)
        self.assertFormError(response, 'form', '__all__',
                             'The username and/or password '
                             'you specified are not correct.')

    def test_POST_incorrect_password(self):
        """
        Anonymous account sends POST request with
        incorrect password.
        """
        data = {
            'login': self.account.username,
            'password': 'incorrect_password'
        }

        response = self.client.post(self.url, data=data)

        self.assertEquals(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertEquals(len(response.context['form'].errors), 1)
        self.assertFormError(response, 'form', '__all__',
                             'The username and/or password '
                             'you specified are not correct.')

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('profile'), 302)


class LogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('logout')

        cls.account = account = get_user_model().objects.create(username='username1')
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        response = self.client.get(reverse('logout'))

        self.assertEquals(response.status_code, 405)

    def test_POST(self):
        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'), 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_authenticated_POST(self):
        self.client.login(username=self.account.username)

        response = self.client.post(reverse('logout'))

        self.assertRedirects(response, reverse('login'), 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class SignupAdministratorViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Account = Account = get_user_model()
        cls.url = reverse('administrator_signup')

        cls.account = account = Account.objects.create(username='username1')
        account.set_password('password_')
        account.save()

        cls.admin = admin = Account.objects.create(
            username='admin', is_staff=True, is_superuser=True)
        admin.set_password('password_')
        admin.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous non-admin account sends GET request."""
        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('login'), 302)

    def test_authenticated_as_non_admin_GET(self):
        """Authenticated non-admin account sends GET request."""
        self.client.login(username=self.account.username, password='password_')

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('login'), status_code=302,
                             fetch_redirect_response=False)

    def test_authenticated_as_admin_GET(self):
        """Authenticated admin sends GET request."""
        self.client.login(username=self.admin.username, password='password_')

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'),
                              SignupAdministratorForm)
        self.assertTemplateUsed(response, 'accounts/signup_administrator.html')

    def test_POST(self):
        """
        Anonymous non-admin account sends
        POST request with correct data.
        """
        data = {
            'email': 'email2@gmail.com',
            'first_name': 'Firstname',
            'last_name': 'Lastname',
            'password1': 'password_',
            'password2': 'password_',
        }

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('login'), status_code=302,
                             fetch_redirect_response=False)
        self.assertEquals(self.Account.objects.count(), 2)

    def test_authenticated_as_non_admin_POST(self):
        """
        Authenticated non-admin account sends POST
        request with correct data.
        """
        data = {
            'email': 'email2@gmail.com',
            'password1': 'password_',
            'password2': 'password_',
        }

        self.client.login(username=self.account.username, password='password_')

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response, reverse('login'), status_code=302,
                             fetch_redirect_response=False)
        self.assertEquals(self.Account.objects.count(), 2)

    def test_authenticated_as_admin_POST_no_data(self):
        """Authenticated admin sends POST request without data."""
        self.client.login(username=self.admin.username, password='password_')

        response = self.client.post(self.url, data={})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 5)
        self.assertFormError(response, 'form', 'email',
                             'This field is required.')
        self.assertFormError(response, 'form', 'first_name',
                             'This field is required.')
        self.assertFormError(response, 'form', 'last_name',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')
        self.assertEquals(self.Account.objects.count(), 2)

    def test_authenticated_as_admin_POST_invalid_data(self):
        """Authenticated admin sends POST request with incorrect data."""
        self.client.login(username=self.admin.username, password='password_')

        response = self.client.post(
            self.url,
            data={
                'email': 'email',
                'password1': 'email',
            },
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['form'].errors), 5)
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')
        self.assertFormError(response, 'form', 'first_name',
                             'This field is required.')
        self.assertFormError(response, 'form', 'last_name',
                             'This field is required.')
        self.assertFormError(
            response, 'form', 'password1',
            [
                'This password is too short. '
                'It must contain at least 8 characters.',
                'This password is too common.',
            ]
        )
        self.assertFormError(response, 'form', 'password2',
                             'This field is required.')
        self.assertEquals(self.Account.objects.count(), 2)

    def test_authenticated_as_admin_POST(self):
        """
        Authenticated admin sends POST request
        with correct data.
        """
        data = {
            'email': 'email2@gmail.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'password_',
            'password2': 'password_',
        }

        self.client.login(username=self.admin.username, password='password_')

        response = self.client.post(self.url, data=data)

        self.assertRedirects(response,
                             reverse('account_email_verification_sent'), 302)
        self.assertEquals(self.Account.objects.count(), 3)

        account = self.Account.objects.last()
        self.assertTrue(account.is_administrator)
        self.assertEquals(account.email, data['email'])
        self.assertEquals(account.first_name, data['first_name'])
        self.assertEquals(account.last_name, data['last_name'])
        self.assertTrue(account.check_password(data['password1']))


class EmailVerificationSentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('account_email_verification_sent')

        cls.account = account = get_user_model().objects.create(
            username='username1')
        account.set_password('password_')
        account.save()

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirm_email_sent.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirm_email_sent.html')

    def test_POST(self):
        """Anonymous account sends POST request."""
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.post(self.url)

        self.assertEquals(response.status_code, 405)


class ConfirmEmailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.account = account = get_user_model().objects.create(email='email1')
        account.set_password('password_')
        account.save()

        email_address = EmailAddress.objects.create(
            user=account,
            email=account.email
        )
        email_confirmation = EmailConfirmation.create(
            email_address=email_address)
        email_confirmation.sent = email_confirmation.created
        email_confirmation.save()

        cls.url = reverse(
            'account_confirm_email',
            args=[email_confirmation.key]
        )

    def setUp(self):
        self.client = Client()

    def test_GET(self):
        """Anonymous account sends GET request."""
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirm_email.html')

    def test_authenticated_GET(self):
        """Authenticated account sends GET request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirm_email.html')

    def test_POST(self):
        """Anonymous account sends POST request."""
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('login'), 302)

    def test_authenticated_POST(self):
        """Authenticated account sends POST request."""
        self.client.login(username=self.account.username, password='password_')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('login'), 302)
