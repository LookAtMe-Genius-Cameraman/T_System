#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's video and audio stream management.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, Response, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.stream import start_stream, stop_stream

api_bp = Blueprint('stream_api', __name__)

api = Api(api_bp)


class StreamApi(Resource):
    """Class to define an API to manage the video and audio stream of T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.get` for getting T_System base OS system info,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.post` INVALID,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.put` INVALID,
         :func:`t_system.remote_ui.api.system_info.SystemInfoApi.delete` INVALID.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.stream.StreamApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        stream_type = request.args.get('type')
        admin_id = request.args.get('admin_id', None)

        if not stream_type:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        stream, mimetype = start_stream(admin_id, stream_type)

        if stream and mimetype:
            return {'status': 'OK', 'data': Response(stream, mimetype=mimetype)}
        else:
            return {'status': 'ERROR', 'message': "FAILED"}

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


api.add_resource(StreamApi, '/api/stream')
