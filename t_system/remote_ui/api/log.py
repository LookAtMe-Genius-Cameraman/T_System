#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: log
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for managing logging ability of T_System

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request, send_file
from flask_restful import Api, Resource

from t_system.remote_ui.modules.log import get_logfile, clear_logs

api_bp = Blueprint('log_api', __name__)
api = Api(api_bp)


class LogApi(Resource):
    """Class to define an API of system info of T_System base OS.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.log.LogApi.get` for getting T_System base OS system info,
         :func:`t_system.remote_ui.api.log.LogApi.post` INVALID,
         :func:`t_system.remote_ui.api.log.LogApi.put` INVALID,
         :func:`t_system.remote_ui.api.log.LogApi.delete` INVALID.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.log.LogApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        admin_id = request.args.get('admin_id', None)

        log_file, file_name = get_logfile(admin_id)

        if log_file and file_name:
            return send_file(log_file, attachment_filename=file_name)
        else:
            return {'status': 'ERROR', 'message': "FAILED"}

    def post(self):
        """The API method to POST request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to GET request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        admin_id = request.args.get('admin_id', None)

        result = clear_logs(admin_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(LogApi, '/api/logging')
