from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from core.decorators import AccountAllower


class AccountAllowerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account = get_user_model()

        cls.user = Account.objects.create()
        cls.administrator = Account.objects.create(is_administrator=True)
        cls.admin = Account.objects.create(is_superuser=True)
        cls.anonymous = AnonymousUser()

        cls.redirect_url = reverse('profile')

        cls.view_func = lambda x: 'Response!'
        cls.request = HttpRequest()

    def test_init(self):
        account_allower = AccountAllower('redirect_url', 'allow_to')
        self.assertEquals(account_allower.redirect_url, 'redirect_url')
        self.assertEquals(account_allower.allow_to, 'allow_to')

    def test_allow_to_user(self):
        """Allows only user to access view."""
        self.request.user = self.user
        response = AccountAllower('', 'user')(self.view_func)
        self.assertEquals(response(self.request), 'Response!')

        bad_accounts = self.administrator, self.admin, self.anonymous

        for bad_account in bad_accounts:
            self.request.user = bad_account

            response = AccountAllower(
                self.redirect_url, 'user')(self.view_func)
            self.assertEquals(
                type(response(self.request)), HttpResponseRedirect)

    def test_allow_to_admin(self):
        """Allows only admin to access view."""
        self.request.user = self.admin
        response = AccountAllower('', 'admin')(self.view_func)
        self.assertEquals(response(self.request), 'Response!')

        bad_accounts = self.administrator, self.user, self.anonymous

        for bad_account in bad_accounts:
            self.request.user = bad_account

            response = AccountAllower(
                self.redirect_url, 'admin')(self.view_func)
            self.assertEquals(
                type(response(self.request)), HttpResponseRedirect)

    def test_allow_to_anonymous(self):
        """Allows only anonymous to access view."""
        self.request.user = self.anonymous
        response = AccountAllower('', 'anonymous')(self.view_func)
        self.assertEquals(response(self.request), 'Response!')

        bad_accounts = self.administrator, self.admin, self.user

        for bad_account in bad_accounts:
            self.request.user = bad_account

            response = AccountAllower(
                self.redirect_url, 'anonymous')(self.view_func)
            self.assertEquals(
                type(response(self.request)), HttpResponseRedirect)
