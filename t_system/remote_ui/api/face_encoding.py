#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoding
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for face encoding of T_System's face recognition ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, request
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.face_encoding import create_face, get_face, get_faces, update_face, delete_face
from t_system.remote_ui.api.data_schema import FACE_ENCODING_SCHEMA

api_bp = Blueprint('face_encoding_api', __name__)
api = Api(api_bp)


class FaceEncodingApi(Resource):
    """Class to define an API of the face encoding ability of T_System.

        This class provides necessary initiations and functions named;
         :func:`t_system.remote_ui.api.face_encoding.FaceEncodingApi.get`for the provide get face data from database,
         :func:`t_system.remote_ui.api.face_encoding.FaceEncodingApi.post` for provide creating new face encoding,
         :func:`t_system.remote_uia.api.face_encoding.FaceEncodingApi.put` for provide updating the putted faces's encodings,
         :func:`t_system.remote_ui.api.face_encoding.FaceEncodingApi.delete` for provide deleting the face.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.api.face_encoding.FaceEncodingApi` class.
        """

    def get(self):
        """The API method to GET request for flask.
        """

        face_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)

        if face_id:
            face = get_face(admin_id, face_id)
            return {'status': 'OK', 'data': face}

        faces = get_faces(admin_id)

        return {'status': 'OK', 'data': faces}

    def post(self):
        """The API method to POST request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        try:
            form = request.form.to_dict(flat=True)
            data = FACE_ENCODING_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result = create_face(admin_id, data)

        return {'status': 'OK' if result else 'ERROR'}

    def put(self):
        """The API method to PUT request for flask.
        """
        face_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not face_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}
        try:
            form = request.form.to_dict(flat=True)
            data = FACE_ENCODING_SCHEMA.validate(form)
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}

        result = update_face(admin_id, face_id, data)
        return {'status': 'OK' if result else 'ERROR'}

    def delete(self):
        """The API method to DELETE request for flask.
        """
        face_id = request.args.get('id')
        admin_id = request.args.get('admin_id', None)

        if not face_id:
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        result = delete_face(admin_id, face_id)

        return {'status': 'OK' if result else 'ERROR'}


api.add_resource(FaceEncodingApi, '/api/face_encoding')
