from functools import wraps

from django.shortcuts import redirect


class AccountAllower:
    """
    Class-decorator for views that allow only
    special type of account to access view.
    """
    def __init__(self, redirect_url: str, allow_to: str):
        self.redirect_url = redirect_url
        self.allow_to = allow_to

    def __call__(self, view_func):
        @wraps(view_func)
        def check(request, *args, **kwargs):
            if request.user.is_authenticated:
                match self.allow_to:
                    case 'user':
                        if not request.user.is_administrator:
                            return view_func(request, *args, **kwargs)
                    case 'admin':
                        if request.user.is_superuser:
                            return view_func(request, *args, **kwargs)
            elif self.allow_to == 'anonymous':
                return view_func(request, *args, **kwargs)
            return redirect(self.redirect_url)
        return check


account_allower = AccountAllower
