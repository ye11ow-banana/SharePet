from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class AccountManager(UserManager):
    """Main `Account` model manager."""
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save an account with the given
        username, email, and password.
        """
        if not username and not email:
            raise ValueError('Username or email must be set')

        email = email if email else None
        if email:
            email = self.normalize_email(email)

        account = self.model(username=username, email=email, **extra_fields)
        account.password = make_password(password)
        account.save(using=self._db)

        return account
