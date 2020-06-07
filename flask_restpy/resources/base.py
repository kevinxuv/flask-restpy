
from typing import List


class Resource(object):

    def to_dict(self) -> dict:
        raise NotImplementedError

    def get_by_id(self, id):
        raise NotImplementedError

    def get(self, *query, **filters):
        raise NotImplementedError

    def create(self, **instance):
        raise NotImplementedError

    def batch_create(self, instances: List[dict]):
        raise NotImplementedError

    def update(self, instance: dict, **filters):
        raise NotImplementedError

    def update_by_id(self, id, **update):
        raise NotImplementedError

    def batch_update(self, instances: List[dict]):
        raise NotImplementedError

    def delete(self, instance):
        raise NotImplementedError

    def delete_by_id(self, id):
        raise NotImplementedError

    def batch_delete(self, instances: List[dict]):
        raise NotImplementedError
