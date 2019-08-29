#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoding
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing the face encoder of t_system's face recognition ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher
from t_system.face_encoding import FaceEncodeManager
from t_system.administration import is_admin

from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_face(admin_id, data):
    """Method to create new face with its encoding pickle data.

    Args:
        admin_id (str):                Root privileges flag.
        data (dict):                    Position data structure.
    """

    # table = get_db_table(admin_id)

    face_encode_manager = FaceEncodeManager()

    face_encode_manager.add_face(data['face_name'], data['photos'])

    result = True

    return result


def get_faces(admin_id):
    """Method to return existing faces.

    Args:
        admin_id (str):                 Root privileges flag.
    """
    try:
        table = get_db_table(is_admin(admin_id))

        result = table.all()  # result = faces

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_face(admin_id, face_id):
    """Method to return existing face and copying its images under the static folder with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        face_id (str):              The id of the position.
    """
    try:
        table = get_db_table(is_admin(admin_id))

        face = table.search((Query().id == face_id))

        if not face:
            result = []
        else:
            # result = [b.to_dict() for b in record]
            face_encode_manager = FaceEncodeManager()
            for face in face_encode_manager.faces:
                if face.id == face_id:
                    face.copy_images_to(f'{T_SYSTEM_PATH}/remote_ui/www/static/images/face_encodings')
            result = [face[0]]

    except Exception as e:
        logger.error(e)
        result = []

    return result


def update_face(admin_id, face_id, data):
    """Method to update the face and its encodings that is recorded in database with given parameters.

    Args:
        admin_id (str):                Root privileges flag.
        face_id (str):                  The id of the position.
        data (dict):                    Position data structure.
    """

    face_encode_manager = FaceEncodeManager()

    result = face_encode_manager.update_face(face_id, data["photos"])

    return result


def delete_face(admin_id, face_id):
    """Method to remove existing face with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        face_id (str):              The id of the position.
    """
    face_encode_manager = FaceEncodeManager()

    result = face_encode_manager.delete_face(face_id)

    return result


def get_db_table(is_admin):
    """Method to set work database.

    Args:
        is_admin (bool):                 Root privileges flag.
    """

    db_folder = f'{dot_t_system_dir}/recognition'
    return DBFetcher(db_folder, "db", "faces").fetch()
