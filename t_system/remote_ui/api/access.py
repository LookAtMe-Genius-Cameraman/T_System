#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: access
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for accessing to the remote_ui itself from client device correctly.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, redirect, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.access import check_private_id, get_private_id_by
from t_system.remote_ui.api.data_schema import ACCESS_SCHEMA

api_bp = Blueprint('access_api', __name__)
api = Api(api_bp)


class AccessApi(Resource):
    """Class to define an API to accessing T_System from remote device.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.access.AccessApi.get` for redirecting to home page of Remote UI,
         :func:`t_system.remote_ui.api.access.AccessApi.post` for sending identity of T_System to requested device,
         :func:`t_system.remote_ui.api.access.AccessApi.put` INVALID
         :func:`t_system.remote_ui.api.access.AccessApi.delete` INVALID
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.access.MoveApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """
        private_id = request.args.get('id')

        if not private_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if check_private_id(private_id):
            return redirect('/')

        return {'status': 'ERROR'}

    def post(self):
        """The API method to POST request for flask.
        """

        try:
            form = request.form.to_dict(flat=True)  # request.form returns an immutable dict. And flat=False convert each value of the keys to list.
            data = ACCESS_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        private_id = get_private_id_by(data)

        return {'status': 'OK', 'data': private_id}

    def put(self):
        """The API method to PUT request for flask.
        """
        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}


api.add_resource(AccessApi, '/api/access')
