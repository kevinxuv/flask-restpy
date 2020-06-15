import logging

from werkzeug.exceptions import BadRequest, NotFound
from flask import (Flask, request, jsonify)
from flask.views import MethodView


from flask_restpy.resources.base import Resource

logger = logging.getLogger(__name__)


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
        body_params = request.get_json()
        if isinstance(body_params, list):
            instances = self.resource.batch_create(body_params)
            res = [instance.to_dict() for instance in instances]
        elif isinstance(body_params, dict):
            instance = self.resource.create(**body_params)
            res = instance.to_dict()
        else:
            raise BadRequest
        return jsonify(res), 201

    def put(self, id):
        body_params = request.get_json()
        if id is not None:
            if not isinstance(body_params, dict):
                raise BadRequest
            instance = self.resource.update_by_id(id, **body_params)
            if not instance:
                raise NotFound
            res = instance.to_dict()
        elif isinstance(body_params, dict):
            instance = self.resource.update(body_params)
            res = instance.to_dict()
        elif isinstance(body_params, list):
            instances = self.resource.batch_update(body_params)
            res = [instance.to_dict() for instance in instances]
        else:
            raise BadRequest
        return jsonify(res)

    def delete(self, id):
        body_params = request.get_json()
        if id is not None:
            instance = self.resource.get_by_id(id)
            if not instance:
                raise NotFound
            self.resource.delete(instance)
        elif isinstance(body_params, dict):
            self.resource.delete(body_params)
        elif isinstance(body_params, list):
            self.resource.batch_delete(body_params)
        else:
            raise BadRequest
        return '', 204


def get_all_resource_views():
    import gc
    resources = [
        kls for kls in gc.get_objects()
        if issubclass(type(kls), type) and issubclass(kls, Resource)
        and kls != Resource and 'Resource' not in kls.__name__
    ]
    logger.debug(resources)
    resource_views = {}
    for resource in resources:
        resource_view = ResourceView(resource)
        resource_view.__name__ = resource.__name__.lower()
        resource_views[f'{resource.__name__.lower()}s'] = resource_view
    return resource_views


def register_restapi(app: Flask, prefix='/api', resource_views: dict = None):
    if resource_views is None:
        resource_views = get_all_resource_views()
    logger.debug(resource_views)
    for resource_path, resource_view in resource_views.items():
        view_func = resource_view.as_view(resource_view.__name__)
        app.add_url_rule(
            f'{prefix}/{resource_path}',
            defaults={'id': None},
            view_func=view_func,
            methods=['GET'])
        app.add_url_rule(
            f'{prefix}/{resource_path}',
            view_func=view_func,
            methods=['POST'])
        app.add_url_rule(
            f'{prefix}/{resource_path}' + '/<int:id>',
            view_func=view_func,
            methods=['GET', 'DELETE', 'PUT'])
