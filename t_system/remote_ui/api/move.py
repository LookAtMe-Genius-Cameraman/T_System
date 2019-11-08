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

from t_system.remote_ui.modules.move import set_arm, move_arm, move_arm_by, get_arm_current_position, get_arm_joint_count
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
        """The API method to GET request for flask.
        """

        cause = request.args.get('cause', None)
        admin_id = request.args.get('admin_id', None)

        if cause == "joint_count":
            joint_count = get_arm_joint_count(admin_id)
            return {'status': 'OK', 'data': joint_count}

        current_position = get_arm_current_position(admin_id)

        return {'status': 'OK', 'data': current_position}

    def post(self):
        """The API method to POST request for flask.
        """

        db_name = request.args.get('db')
        action = request.args.get('action')
        a_type = request.args.get('a_type')
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not db_name:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if not action:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if not a_type:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        move_arm_by(admin_id, root, db_name, action, a_type)

        return {'status': 'OK'}

    def put(self):
        """The API method to PUT request for flask.
        """
        move_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not move_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = MOVE_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = move_arm(admin_id, move_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def patch(self):
        """The API method to PATCH request for flask.
        """
        expand = request.args.get('expand')
        admin_id = request.args.get('admin_id', None)

        if not expand:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        set_arm(admin_id, expand)

        return {'status': 'OK'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(MoveApi, '/api/move')
