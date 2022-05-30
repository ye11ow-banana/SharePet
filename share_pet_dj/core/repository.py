from typing import TypeVar

from django.db.models.base import ModelBase, Model
from django.forms import model_to_dict

T = TypeVar('T', bound=Model)


class ModelObjectUpdate:
    """Logic for updating model object."""
    def __init__(self, model: T):
        self.model = model

    def update_fields_by_pk(self, pk: int, **kwargs) -> None:
        self.model.objects.filter(pk=pk).update(**kwargs)


class ModelObjectGet:
    """Logic for getting model object."""
    def __init__(self, model: T):
        self.model = model

    def _get_model_object(self, *args, **kwargs) -> ModelBase:
        return self.model.objects.get(*args, **kwargs)

    @staticmethod
    def _get_model_object_with_fields(
            model_object: ModelBase, fields: tuple) -> dict:
        return model_to_dict(model_object, fields=fields)

    def get_model_object(self, fields: tuple, **kwargs) -> dict:
        model_object = self._get_model_object(**kwargs)
        return self._get_model_object_with_fields(model_object, fields)

    def get_pure_model_object(self, *args, **kwargs) -> ModelBase:
        return self._get_model_object(*args, **kwargs)


class ModelObject(ModelObjectGet, ModelObjectUpdate):
    """Logic for model object."""
