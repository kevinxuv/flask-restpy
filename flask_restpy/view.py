from typing import List

from werkzeug.exceptions import BadRequest, NotFound
from flask import (Flask, request, jsonify)
from flask.views import MethodView


from flask_restpy.resources.base import Resource


class ResourceView(MethodView):

    def __init__(self, resource: Resource):
        self.resource = resource

    def get(self, id):
        if id is not None:
            instance = self.resource.get_by_id(id)
            if not instance:
                raise NotFound
            res = instance.to_dict()
        else:
            instances = self.resource.get(**request.args)
            res = [instance.to_dict() for instance in instances]
        return jsonify(res)

    def post(self):
        request_body = request.get_json()
        if isinstance(request_body, list):
            instances = self.resource.batch_create(request_body)
            res = [instance.to_dict() for instance in instances]
        elif isinstance(request_body, dict):
            instance = self.resource.create(**request_body)
            res = instance.to_dict()
        else:
            raise BadRequest
        return jsonify(res), 201

    def put(self, id):
        request_body = request.get_json()
        if id is not None:
            if not isinstance(request_body, dict):
                raise BadRequest
            instance = self.resource.update_by_id(id, **request_body)
            if not instance:
                raise NotFound
            res = instance.to_dict()
        elif isinstance(request_body, dict):
            instance = self.resource.update(request_body)
            res = instance.to_dict()
        elif isinstance(request_body, list):
            instances = self.resource.batch_update(request_body)
            res = [instance.to_dict() for instance in instances]
        else:
            raise BadRequest
        return jsonify(res)

    def delete(self, id):
        request_body = request.get_json()
        if id is not None:
            instance = self.resource.get_by_id(id)
            if not instance:
                raise NotFound
            self.resource.delete(instance)
        elif isinstance(request_body, dict):
            self.resource.delete(request_body)
        elif isinstance(request_body, list):
            self.resource.batch_delete(request_body)
        else:
            raise BadRequest
        return '', 204


def get_all_resource_views():
    import gc
    resouces = [
        kls for kls in gc.get_objects()
        if issubclass(type(kls), type) and issubclass(kls, Resource)
        and kls != Resource and 'Resource' not in kls.__name__
    ]
    resource_views = {}
    for resouce in resouces:
        resource_view = ResourceView(resouce)
        resource_views[f'{resouce.__name__.upper()}s'] = resource_view
    return resource_views


def register_restapi(app: Flask, resource_views: List[ResourceView] = None):
    if resource_views is None:
        resource_views = get_all_resource_views()
    for resource_path, resource_view in resource_views.items():
        view_func = resource_view.as_view(resource_view.__name__)
        app.add_url_rule(
            resource_path,
            defaults={'id': None},
            view_func=view_func,
            methods=['GET'])
        app.add_url_rule(
            resource_path,
            view_func=view_func,
            methods=['POST'])
        app.add_url_rule(
            resource_path + '/<int:id>',
            view_func=view_func,
            methods=['GET', 'DELETE', 'PUT'])
