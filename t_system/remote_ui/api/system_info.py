#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for getting information of T_System's base OS.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.system_info import get_system_info
from t_system.remote_ui.api.data_schema import SCENARIO_SCHEMA

api_bp = Blueprint('system_info_api', __name__)

api = Api(api_bp)


class SystemInfoApi(Resource):
    """Class to define an API of system info of T_System base OS.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.get` for getting T_System base OS system info,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.post` INVALID,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.put` INVALID,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.delete` INVALID.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.system_info.SystemInfoApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        admin_id = request.args.get('admin_id', None)

        system_info = get_system_info(admin_id)
        return {'status': 'OK', 'data': system_info}

    def post(self):
        """The API method to post request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to get request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def delete(self):
        """The API method to delete request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(SystemInfoApi, '/api/system_info')
