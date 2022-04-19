from django.test import SimpleTestCase
from django.urls import resolve, reverse

from accounts import views


class TestUrls(SimpleTestCase):
    """Test urls routers of `accounts` app."""
    def test_user_signup_url_is_resolved(self):
        url = reverse('user_signup')
        self.assertEquals(resolve(url).func, views.signup_user)

    def test_password_reset_url_is_resolved(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func, views.password_reset)

    def test_password_reset_done_url_is_resolved(self):
        url = reverse('account_reset_password_done')
        self.assertEquals(resolve(url).func, views.password_reset_done)

    def test_reset_password_from_key_url_is_resolved(self):
        url = reverse(
            'account_reset_password_from_key',
            kwargs={'uidb36': '1d',
                    'key': 'b3mliu-a5699bb9b46d416445de6637402355d5'}
        )
        self.assertEquals(resolve(url).func, views.password_reset_from_key)

    def test_password_reset_from_key_done_url_is_resolved(self):
        url = reverse('account_reset_password_from_key_done')
        self.assertEquals(resolve(url).func,
                          views.password_reset_from_key_done)

    def test_password_change_url_is_resolved(self):
        url = reverse('password_change')
        self.assertEquals(resolve(url).func, views.change_password)

    def test_user_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, views.login)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, views.logout)

    def test_administrator_signup_url_is_resolved(self):
        url = reverse('administrator_signup')
        self.assertEquals(resolve(url).func, views.signup_administrator)

    def test_email_verification_sent_url_is_resolved(self):
        url = reverse('account_email_verification_sent')
        self.assertEquals(resolve(url).func, views.email_verification_sent)

    def test_confirm_email_url_is_resolved(self):
        url = reverse(
            'account_confirm_email',
            kwargs={'key': 'NDU:1ncMz3:BZSAf34XxZi_'
                           'd8KwH9po_ngPkoQwgiuhQDtql9RKcvQ'}
        )
        self.assertEquals(resolve(url).func, views.confirm_email)

    def test_profile_url_is_resolved(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, views.check)
