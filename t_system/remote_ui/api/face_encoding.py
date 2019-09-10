#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoding
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the API for face encoding of T_System's face recognition ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Blueprint, Response, request, send_file
from flask_restful import Api, Resource
from schema import SchemaError

from t_system.remote_ui.modules.face_encoding import create_face, get_face_image, download_face_image, get_faces, update_face, delete_face
from t_system.remote_ui.api.data_schema import FACE_ENCODING_SCHEMA

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

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

        is_download = request.args.get('download', None)
        face_image = request.args.get('image', None)
        face_id = request.args.get('id', None)
        admin_id = request.args.get('admin_id', None)

        if not face_id and (face_image or is_download):
            return {'status': 'ERROR', 'message': '\'id\' parameter is missing'}

        if face_id and not face_image:
            return {'status': 'ERROR', 'message': '\'image\' parameter is missing'}

        if face_id:
            if is_download:

                image = download_face_image(admin_id, face_id, face_image)
                if not image:
                    return {'status': 'ERROR', 'message': 'parameter invalid'}

                return send_file(image)
            else:
                image, mimetype = get_face_image(admin_id, face_id, face_image)
                if image and mimetype:
                    logger.debug("Response returning")
                    return Response(image, mimetype=mimetype)

        faces = get_faces(admin_id)

        return {'status': 'OK', 'data': faces}

    def post(self):
        """The API method to POST request for flask.
        """
        admin_id = request.args.get('admin_id', None)

        try:
            name = request.form.to_dict(flat=True).get("face_name")
            images = request.files.getlist("face_images")
        except SchemaError as e:
            return {'status': 'ERROR', 'message': e.code}
        result = create_face(admin_id, name, images)

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
