from core.repository import ModelObject
from notifications.models import Notification


class NotificationUpdate:
    """Logic for updating `Notification` model."""
    _model_object = ModelObject(Notification)

    def update_fields_by_pk(self, pk: int, **kwargs) -> None:
        self._model_object.update_fields_by_pk(pk, **kwargs)


class NotificationGet:
    """Logic for getting `Notification` model."""
    _model_object = ModelObject(Notification)

    def get_notification(self, fields: tuple, **kwargs: int) -> dict:
        return self._model_object.get_model_object(fields, **kwargs)


class NotificationRepository(NotificationGet, NotificationUpdate):
    """Logic for `Notification` model."""
