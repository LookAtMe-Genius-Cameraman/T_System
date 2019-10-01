#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoding
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing the face encoder of t_system's face recognition ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import log_manager
from t_system import face_encode_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_face(admin_id, name, images):
    """Method to create new face with its encoding pickle data.

    Args:
        admin_id (str):                Root privileges flag.
        name (str):                    Name of the images owner face.
        images (list):                 list of FileStorage object.
    """

    from t_system.remote_ui import allowed_file

    for image in images:
        if not allowed_file(image.filename, {'png', 'jpg', 'jpeg'}):
            images.remove(image)

    face_encode_manager.add_face(name, set(images))
    result = True

    return result


def get_faces(admin_id):
    """Method to return existing faces.

    Args:
        admin_id (str):                 Root privileges flag.
    """

    result = []
    try:

        faces = face_encode_manager.get_faces()

        if faces:
            for face in faces:
                result.append({"id": face.id, "name": face.name, "image_names": face.image_names})

    except Exception as e:
        logger.error(e)
        result = []
    logger.debug(str(result))
    return result


def get_face_image(admin_id, face_id, image_name):
    """Method to return existing face and copying its images under the static folder with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        face_id (str):                  The id of the face.
        image_name (str):               Name of the one of face images that is wanted.
    """

    face = face_encode_manager.get_face(face_id)

    if not face:
        return None, None

    if image_name in face.image_names:
        image_path = f'{face.dataset_folder}/{image_name}'
        image_extension = image_name.rsplit('.', 1)[1].lower()
    else:
        return None, None

    return open(image_path, 'rb'), f'image/{image_extension};'


def download_face_image(admin_id, face_id, image_name):
    """Method to return existing face and copying its images under the static folder with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        face_id (str):                  The id of the face.
        image_name (str):               Name of the one of face images that is wanted.
    """

    result = ""
    try:

        face = face_encode_manager.get_face(face_id)

        if face:
            if image_name in face.image_names:
                result = f'{face.dataset_folder}/{image_name}'

    except Exception as e:
        logger.error(e)
        result = ""

    return result


def update_face(admin_id, face_id, data):
    """Method to update the face and its encodings that is recorded in database with given parameters.

    Args:
        admin_id (str):                Root privileges flag.
        face_id (str):                  The id of the position.
        data (dict):                    Position data structure.
    """

    result = face_encode_manager.update_face(face_id, data["photos"])

    return result


def delete_face(admin_id, face_id):
    """Method to remove existing face with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        face_id (str):              The id of the position.
    """

    result = face_encode_manager.delete_face(face_id)

    return result
