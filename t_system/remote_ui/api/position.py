#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's arm positions.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.position import create_position, get_position, get_positions, update_position, delete_position
from t_system.remote_ui.api.data_schema import POSITION_SCHEMA

api_bp = Blueprint('position_api', __name__)
api = Api(api_bp)


class PositionApi(Resource):
    """Class to define an API of the positions of the arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.position.PositionApi.get`for the provide get position data from database,
         :func:`t_system.remote_ui.api.position.PositionApi.post` for provide creating new position,
         :func:`t_system.remote_uia.api.position.PositionApi.put` for provide updating the position,
         :func:`t_system.remote_ui.api.position.PositionApi.delete` for provide deleting the position.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.position.PositionApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        db_name = request.args.get('db')
        position_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)

        if not db_name:
            return {'status': 'ERROR', 'message': '\'db\' parameter is missing'}

        if position_id:
            position = get_position(admin_id, db_name, position_id)
            return {'status': 'OK', 'data': position}

        positions = get_positions(admin_id, db_name)

        return {'status': 'OK', 'data': positions}

    def post(self):
        """The API method to post request for flask.
        """
        db_name = request.args.get('db')
        admin_id = request.args.get('admin_id', None)

        if not db_name:
            return {'status': 'ERROR', 'message': '\'db\' parameter is missing'}

        try:
            form = request.form.to_dict(flat=True)
            data = POSITION_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result, position_id = create_position(admin_id, db_name, data)

        return {'status': 'OK' if result else 'ERROR', 'id': position_id}

    def put(self):
        """The API method to put request for flask.
        """
        db_name = request.args.get('db')
        position_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not db_name:
            return {'status': 'ERROR', 'message': '\'db\' parameter is missing'}

        if not position_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = POSITION_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_position(admin_id, db_name, position_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """

        db_name = request.args.get('db')
        position_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not db_name:
            return {'status': 'ERROR', 'message': '\'db\' parameter is missing'}

        if not position_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        result = delete_position(admin_id, db_name, position_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(PositionApi, '/api/position')
