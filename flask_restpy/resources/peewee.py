
from typing import List

from peewee import Model
from playhouse.shortcuts import model_to_dict

from .base import Resource
from flask_restpy.exceptions import ParamError


class PeeweeResource(Resource):

    def __init__(self, model: Model):
        self.model = model

    def to_dict(self):
        return model_to_dict(self)

    def get_by_id(self, id):
        return self.model.get_by_id(id)

    def get(self, *fields, page=None, limit=None, **filters):
        for field in fields:
            if not hasattr(self.model, field):
                raise ParamError(f'{field} not in model {self.model}')
        sq = self.model.select(*fields)
        for field, value in filters.items():
            if not hasattr(self.model, field):
                raise ParamError(f'{field} not in model {self.model}')
            sq = sq.where(getattr(self.model, field) == value)
        if page and limit:
            sq = sq.paginate(page=page, paginate_by=limit)
        else:
            sq = sq.paginate(1)
        return list(sq)

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
