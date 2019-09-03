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

from t_system.remote_ui.modules.stream import StreamManager

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

stream_manager = StreamManager()

api_bp = Blueprint('stream_api', __name__)
api = Api(api_bp)


class StreamApi(Resource):
    """Class to define an API to manage the video and audio stream of T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.stream.StreamApi.get` for getting video stream of t_system's vision,
         :func:`t_system.remote_ui.api.stream.StreamApi.post` INVALID,
         :func:`t_system.remote_ui.api.stream.StreamApi.put` INVALID,
         :func:`t_system.remote_ui.api.stream.StreamApi.delete` for stopping video stream.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.stream.StreamApi` class.
        """
        # Class has been creating again for each request.
        pass

    def get(self):
        """The API method to GET request for flask.
        """

        stream_type = request.args.get('type')
        admin_id = request.args.get('admin_id', None)

        if not stream_type:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        stream, mimetype = stream_manager.start_stream(admin_id, stream_type)

        if stream and mimetype:
            logger.debug("Response returning")
            return Response(stream(), mimetype=mimetype)
            # return {'status': 'OK', 'data': str(Response(stream(), mimetype=mimetype))}
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

        stream_type = request.args.get('type')
        admin_id = request.args.get('admin_id', None)

        if not stream_type:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        logger.debug("DELETE request triggered")
        result = stream_manager.stop_stream(admin_id, stream_type)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(StreamApi, '/api/stream')
