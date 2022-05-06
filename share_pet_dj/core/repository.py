from typing import Generator

from django.db.models.base import ModelBase
from django.forms import model_to_dict

from accounts.services.dataclasses import AccountData


class ModelObjectUpdate:
    """Logic for updating model object."""
    def update_fields_by_pk(self, pk: int, **kwargs) -> None:
        self.model.objects.filter(pk=pk).update(**kwargs)


class ModelObjectGet:
    """Logic for getting model object."""
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

    def get_all_with_fields(
            self, fields: tuple
    ) -> Generator[AccountData, None, None]:
        for model in self.model.objects.values(*fields):
            # todo: other fields
            yield AccountData(
                pk=model.get('id'),
                username=model.get('username'),
            )


class ModelObject(ModelObjectGet, ModelObjectUpdate):
    """Logic for model object."""
    def __init__(self, model: ModelBase):
        self.model = model
