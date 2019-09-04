#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: record
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for handling T_System's video records.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.record import get_record_dates, get_record, get_records, update_record, delete_record
from t_system.remote_ui.api.data_schema import RECORD_SCHEMA

api_bp = Blueprint('record_api', __name__)
api = Api(api_bp)


class RecordApi(Resource):
    """Class to define an API to motion of the t_system's arm.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.record.RecordApi.get` for getting record dates, time and record itself,
         :func:`t_system.remote_ui.api.record.RecordApi.post` INVALID,
         :func:`t_system.remote_ui.api.record.RecordApi.put` for updating record name,
         :func:`t_system.remote_ui.api.record.RecordApi.delete` for deleting record with send id
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.record.RecordApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        records_date = request.args.get('date', None)
        record_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)

        if records_date and record_id:
            return {'status': 'ERROR', 'message': '\'date\' and \'id\' parameter giving together'}

        if not records_date and not record_id:
            record_dates = get_record_dates(admin_id)
            return {'status': 'OK', 'data': record_dates}

        elif records_date:
            records = get_records(admin_id, records_date)
            return {'status': 'OK', 'data': records}

        elif record_id:
            record = get_record(admin_id, record_id)
            return {'status': 'OK', 'data': record}

    def post(self):
        """The API method to POST request for flask.
        """

        return {'status': 'ERROR', 'message': 'NOT VALID'}

    def put(self):
        """The API method to PUT request for flask.
        """

        record_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not record_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = RECORD_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_record(admin_id, record_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """
        record_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not record_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        result = delete_record(admin_id, record_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(RecordApi, '/api/record')
