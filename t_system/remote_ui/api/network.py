#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: network
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System's external network connection ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""


from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.network import create_network, get_networks, get_network, update_network, delete_network
from t_system.remote_ui.api.data_schema import NETWORK_SCHEMA

api_bp = Blueprint('network_api', __name__)

api = Api(api_bp)


class NetworkApi(Resource):
    """Class to define an API to the network connections of the T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.network.NetworkApi.get`for the provide get network connection data from database,
         :func:`t_system.remote_ui.api.network.NetworkApi.post` for provide creating new network connection,
         :func:`t_system.remote_ui.api.network.NetworkApi.put` for provide updating the network connection,
         :func:`t_system.remote_ui.api.network.NetworkApi.delete` for provide deleting the network connection
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.network.NetworkApi` class.
        """

    def get(self):
        """The API method to get request for flask.
        """

        network_ssid = request.args.get('ssid', None)
        admin_id = request.args.get('admin_id', None)

        if network_ssid:
            scenario = get_network(admin_id, network_ssid)
            return {'status': 'OK', 'data': scenario}

        scenarios = get_networks(admin_id)

        return {'status': 'OK', 'data': scenarios}

    def post(self):
        """The API method to post request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        try:
            form = request.form.to_dict(flat=True)  # request.form returns an immutable dict. And flat=False convert each value of the keys to list.
            data = NETWORK_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result, admin_id = create_network(admin_id, data)

        return {'status': 'OK' if result else 'ERROR', 'admin_id': admin_id if admin_id else False}

    def put(self):
        """The API method to put request for flask.
        """
        network_ssid = request.args.get('ssid')
        admin_id = request.args.get('admin_id', None)

        if not network_ssid:
            return {'status': 'ERROR', 'message': '\'ssid\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = NETWORK_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_network(admin_id, network_ssid, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """
        network_ssid = request.args.get('ssid')
        admin_id = request.args.get('admin_id', None)

        if not network_ssid:
            return {'status': 'ERROR', 'message': '\'ssid\' parameter is missing'}

        result = delete_network(admin_id, network_ssid)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(NetworkApi, '/api/network')
