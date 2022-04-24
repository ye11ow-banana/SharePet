"""
This module is used for working with datas.

For example, APIs, Django ORM, SQLAlchemy or another.
"""
from .models import Notification


class NotificationData:
    @staticmethod
    def create(*args, **kwargs) -> Notification:
        return Notification.objects.create(*args, **kwargs)
