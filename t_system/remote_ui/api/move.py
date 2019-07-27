#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: move
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's arm motion with joints or axes.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.move import move_arm
from t_system.remote_ui.api.data_schema import MOVE_SCHEMA

api_bp = Blueprint('move_api', __name__)

api = Api(api_bp)


class MoveApi(Resource):
    """Class to define an API to motion of the t_system's arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.move.MoveApi.get` INVALID,
         :func:`t_system.remote_ui.api.move.MoveApi.post` INVALID,
         :func:`t_system.remote_ui.api.move.MoveApi.put` for moving the t_system's arm,
         :func:`t_system.remote_ui.api.move.MoveApi.delete` INVALID
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.move.MoveApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def post(self):
        """The API method to post request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to put request for flask.
        """
        move_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not move_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            data = MOVE_SCHEMA.validate(request.form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = move_arm(admin_id, move_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(MoveApi, '/api/move')
