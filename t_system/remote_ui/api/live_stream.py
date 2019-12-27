#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: live_stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for T_System Vision's live Stream ability to several Websites.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.live_stream import switch_live_stream, is_stream_available, set_website_usage_status, set_stream_id_u_status, upsert_website, get_website, get_websites, delete_website, create_stream_id, update_stream_id, delete_stream_id
from t_system.remote_ui.api.data_schema import L_STREAM_SCHEMA, L_S_WEBSITE_SCHEMA

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

api_bp = Blueprint('live_stream_api', __name__)
api = Api(api_bp)


class LiveStreamApi(Resource):
    """Class to define an API of the Live Stream ability of T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.live_stream.LiveStreamApi.get`for the provide get live_stream data from database,
         :func:`t_system.remote_ui.api.live_stream.LiveStreamApi.post` for provide creating new Websites and Stream IDs,
         :func:`t_system.remote_uia.api.live_stream.LiveStreamApi.put` for provide updating the Websites and Stream IDs,
         :func:`t_system.remote_ui.api.live_stream.LiveStreamApi.delete` for provide deleting the Websites and Stream IDs.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.live_stream.LiveStreamApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        cause = request.args.get('cause', None)
        website_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if cause == "availability":
            return {'status': 'OK', 'data': is_stream_available(admin_id)}

        if website_id:
            website = get_website(admin_id, root, website_id)
            return {'status': 'OK', 'data': website}

        websites = get_websites(admin_id, root)

        return {'status': 'OK', 'data': websites}

    def post(self):
        """The API method to POST request for flask.
        """
        website_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not website_id:
            try:
                data = L_S_WEBSITE_SCHEMA.validate(request.json)
            except SchemaError as e:
                return {'status': 'ERROR', 'message': e.code}

            result = upsert_website(admin_id, root, data)

            return {'status': 'OK' if result else 'ERROR'}

        try:
            data = L_STREAM_SCHEMA.validate(request.json)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        logger.debug("stream ID creation starting...")

        result = create_stream_id(admin_id, root, website_id, data)

        return {'status': 'OK' if result else 'ERROR'}

    def put(self):
        """The API method to PUT request for flask.
        """
        website_id = request.args.get('id')
        account_name = request.args.get('account_name', None)
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not website_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if account_name:
            try:
                data = L_STREAM_SCHEMA.validate(request.json)
            except SchemaError as e:
                return {'status': 'ERROR', 'message': e.code}

            result = update_stream_id(admin_id, root, website_id, data)
        else:
            try:
                data = L_S_WEBSITE_SCHEMA.validate(request.json)
            except SchemaError as e:
                return {'status': 'ERROR', 'message': e.code}

            result = upsert_website(admin_id, root, data, force_insert=True)

        return {'status': 'OK' if result else 'ERROR'}

    def patch(self):
        """The API method to PATCH request for flask.
        """
        cause = request.args.get('cause')
        in_use = request.args.get('in_use')
        website_id = request.args.get('id', None)
        account_name = request.args.get('account_name', None)
        admin_id = request.args.get('admin_id', None)

        result = False

        if not cause:
            return {'status': 'ERROR', 'message': '\'cause\' parameter is missing'}

        if not in_use:
            return {'status': 'ERROR', 'message': '\'cause\' parameter is missing'}

        if cause == "website":
            result = set_website_usage_status(admin_id, website_id, in_use)
        elif cause == "stream_id":
            result = set_stream_id_u_status(admin_id, website_id, account_name, in_use)
        elif cause == "live":
            result = switch_live_stream(admin_id, in_use)

        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """

        website_id = request.args.get('id')
        account_name = request.args.get('account_name', None)
        admin_id = request.args.get('admin_id', None)
        root = request.args.get('root', None)

        if not website_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if account_name:
            result = delete_stream_id(admin_id, root, website_id, account_name)
        else:
            result = delete_website(admin_id, root, website_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(LiveStreamApi, '/api/live_stream')
