#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: r_sync
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System remote storage folder synchronizations.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.r_sync import sync, set_service_usage_status, set_account_u_status, get_service, get_services, create_account, update_account, delete_account
from t_system.remote_ui.api.data_schema import SYNC_ACCOUNT_SCHEMA

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

api_bp = Blueprint('r_sync_api', __name__)
api = Api(api_bp)


class RSyncApi(Resource):
    """Class to define an API of the Live Stream ability of T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.live_stream.RSyncApi.get`for the provide get r_sync data from database,
         :func:`t_system.remote_ui.api.live_stream.RSyncApi.post` for provide creating new accounts on remote synchronization services,
         :func:`t_system.remote_uia.api.live_stream.RSyncApi.put` for provide updating the accounts of remote synchronization services,
         :func:`t_system.remote_ui.api.live_stream.RSyncApi.delete` for provide deleting the accounts of remote synchronization services.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.live_stream.RSyncApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        service_name = request.args.get('name', None)
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if service_name:
            website = get_service(admin_id, root, service_name)
            return {'status': 'OK', 'data': website}

        websites = get_services(admin_id, root)

        return {'status': 'OK', 'data': websites}

    def post(self):
        """The API method to POST request for flask.
        """
        service_name = request.args.get('name')
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not service_name:
            return {'status': 'ERROR', 'message': '\'name\' parameter is missing'}

        try:
            data = SYNC_ACCOUNT_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = create_account(admin_id, root, service_name, data)

        return {'status': 'OK' if result else 'ERROR'}

    def put(self):
        """The API method to PUT request for flask.
        """
        service_name = request.args.get('name')
        account_name = request.args.get('account_name')
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not service_name:
            return {'status': 'ERROR', 'message': '\'name\' parameter is missing'}

        if not account_name:
            return {'status': 'ERROR', 'message': '\'account_name\' parameter is missing'}

        try:
            data = SYNC_ACCOUNT_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_account(admin_id, root, service_name, data)

        return {'status': 'OK' if result else 'ERROR'}

    def patch(self):
        """The API method to PATCH request for flask.
        """
        cause = request.args.get('cause')
        in_use = request.args.get('in_use')
        service_name = request.args.get('name', None)
        account_name = request.args.get('account_name', None)
        admin_id = request.args.get('admin_id', None)

        result = False

        if not cause:
            return {'status': 'ERROR', 'message': '\'cause\' parameter is missing'}

        if not in_use:
            return {'status': 'ERROR', 'message': '\'cause\' parameter is missing'}

        if cause == "service":
            result = set_service_usage_status(admin_id, service_name, in_use)
        elif cause == "account":
            result = set_account_u_status(admin_id, service_name, account_name, in_use)
        elif cause == "sync":
            result = sync(admin_id, in_use)

        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        service_name = request.args.get('name')
        account_name = request.args.get('account_name')
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not service_name:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if not account_name:
            return {'status': 'ERROR', 'message': '\'account_name\' parameter is missing'}

        result = delete_account(admin_id, root, service_name, account_name)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(RSyncApi, '/api/r_sync')
