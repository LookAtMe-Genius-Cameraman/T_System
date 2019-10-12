#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: identity
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for realize identity processes of T_System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, redirect, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.identity import get_identity_info, update_identity
from t_system.remote_ui.api.data_schema import IDENTITY_SCHEMA

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

api_bp = Blueprint('identity_api', __name__)
api = Api(api_bp)


class IdentityApi(Resource):
    """Class to define an API to accessing T_System from remote device.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.identity.IdentityApi.get` for getting T_System's identity data,
         :func:`t_system.remote_ui.api.identity.IdentityApi.post` INVALID,
         :func:`t_system.remote_ui.api.identity.IdentityApi.put` for updating identity of T_System,
         :func:`t_system.remote_ui.api.identity.IdentityApi.delete` INVALID
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.identity.IdentityApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        identity_info = get_identity_info(admin_id)

        return {'status': 'OK', 'data': identity_info}

    def post(self):
        """The API method to POST request for flask.
        """
        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to PUT request for flask.
        """
        admin_id = request.args.get('admin_id', None)
        cause = request.args.get('cause', None)

        try:
            data = IDENTITY_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_identity(admin_id, cause, data)

        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(IdentityApi, '/api/identity')
