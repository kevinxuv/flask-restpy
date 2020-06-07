
from typing import List

from peewee import Model
from playhouse.shortcuts import model_to_dict

from .base import Resource


class PeeweeResource(Resource):

    def __init__(self, model: Model):
        self.model = model

    def to_dict(self):
        return model_to_dict(self)

    def get_by_id(self, id):
        return self.model.get_by_id(id)

    def get(self, *query, **filters):
        return self.model.get(*query, **filters)

    def create(self, **instance):
        return self.model.create(**instance)

    def batch_create(self, instances: List[dict]):
        return self.model.bulk_create(instances)

    def update(self, instance: dict, **filters):
        instances = self.model.get(**filters)
        for ins in instances:
            self.model.update(**instance).where(self.model.id == ins.id).execute()
        return self.model.get(**filters)

    def update_by_id(self, id, **update):
        self.model.update(**update).where(self.model.id == id).execute()
        return self.model.get_by_id(id)

    def batch_update(self, instances: List[dict]):
        pass

    def delete_by_id(self, id):
        return self.model.delete_by_id(id)

    def delete(self, instance):
        pk = instance.get('id')
        if not pk:
            raise Exception('pk not found')
        return self.model.delete_by_id(pk)

    def batch_delete(self, instances: List[dict]):
        for instance in instances:
            pk = instance.get('id')
            if not pk:
                raise Exception('pk not found')
            self.model.delete_by_id(pk)
