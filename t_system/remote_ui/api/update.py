#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: update
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's self update ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.update import create_position, get_position, get_status, update_status, delete_position
from t_system.remote_ui.api.data_schema import UPDATE_SCHEMA

api_bp = Blueprint('update_api', __name__)

api = Api(api_bp)


class UpdateApi(Resource):
    """Class to define an API of the positions of the arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.update.UpdateApi.get`for the provide get auto-update status and start update with getting finished status,
         :func:`t_system.remote_ui.api.update.UpdateApi.post` INVALID,
         :func:`t_system.remote_uia.api.update.UpdateApi.put` for provide updating the auto-update status,
         :func:`t_system.remote_ui.api.update.UpdateApi.delete` INVALID
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.update.UpdateApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        update_key = request.args.get('key')
        admin_id = request.args.get('admin_id', None)

        if not update_key:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        status = get_status(admin_id, update_key)

        return {'status': 'OK', 'data': status}

    def post(self):
        """The API method to post request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to put request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        form = request.form.to_dict(flat=True)
        data = UPDATE_SCHEMA.validate(form)

        result = update_status(admin_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(UpdateApi, '/api/update')
