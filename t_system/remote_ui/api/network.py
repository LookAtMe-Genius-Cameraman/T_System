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
        is_root = request.args.get('is_root', None)

        if network_ssid:
            scenario = get_network(is_root, network_ssid)
            return {'status': 'OK', 'data': scenario}

        scenarios = get_networks(is_root)

        return {'status': 'OK', 'data': scenarios}

    def post(self):
        """The API method to post request for flask.
        """
        is_root = request.args.get('is_root', None)

        try:
            data = NETWORK_SCHEMA.validate(request.form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result, is_root = create_network(is_root, data)

        return {'status': 'OK' if result else 'ERROR', 'is_root': 'true' if is_root else "false"}

    def put(self):
        """The API method to put request for flask.
        """
        network_ssid = request.args.get('ssid')
        is_root = request.args.get('is_root', None)

        if not network_ssid:
            return {'status': 'ERROR', 'message': '\'ssid\' parameter is missing'}
        try:
            data = NETWORK_SCHEMA.validate(request.form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_network(is_root, network_ssid, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to delete request for flask.
        """
        network_ssid = request.args.get('ssid')
        is_root = request.args.get('is_root', None)

        if not network_ssid:
            return {'status': 'ERROR', 'message': '\'ssid\' parameter is missing'}

        result = delete_network(is_root, network_ssid)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(NetworkApi, '/api/network')
