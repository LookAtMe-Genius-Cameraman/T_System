#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher
from t_system.motion.action import Position
from t_system.administration import is_admin

from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import mission_manager, emotion_manager
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_position(admin_id, root, db_name, data):
    """Method to create new position.

    Args:
        admin_id (str):                 Admin privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        data (dict):                    Position data structure.
    """

    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        position = Position(name=data['name'], cartesian_coords=data['cartesian_coords'], polar_params=data['polar_params'], root=root, db_name=db_name)
        position_id = position.id

        deterfresh_manager(root, db_name)

        result = True
    except Exception:
        result = False
        position_id = None

    return result, position_id


def get_positions(admin_id, root, db_name):
    """Method to return existing positions.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
    """
    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        table = get_db_table(root, db_name)

        result = table.all()  # result = positions

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_position(admin_id, root, db_name, position_id):
    """Method to return existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
    """
    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        table = get_db_table(root, db_name)
        position = table.search((Query().id == position_id))

        if not position:
            result = []
        else:
            result = [position[0]]
    except Exception as e:
        logger.error(e)
        result = []

    return result


def update_position(admin_id, root, db_name, position_id, data):
    """Method to update the position that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
        data (dict):                    Position data structure.
    """

    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    table = get_db_table(root, db_name)
    position = table.search((Query().id == position_id))

    if not position:
        result = False
    else:
        try:
            table.update({'name': data['name'], 'cartesian_coords': data['cartesian_coords'], 'polar_coords': data['polar_coords']}, Query().id == position_id)
            deterfresh_manager(root, db_name)
            result = True
        except Exception:
            result = False

    return result


def delete_position(admin_id, root, db_name, position_id):
    """Method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
    """
    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    table = get_db_table(root, db_name)

    if table.search((Query().id == position_id)):
        table.remove((Query().id == position_id))
        deterfresh_manager(root, db_name)
        result = True
    else:
        result = False

    return result


def get_db_table(root, db_name):
    """Method to set work database by root.

    Args:
        root (bool):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
    """
    table = "positions"
    if root:
        db_folder = f'{T_SYSTEM_PATH}/motion/action'
        return DBFetcher(db_folder, db_name, table).fetch()
    else:
        db_folder = dot_t_system_dir
        db_name = 'missions'
        return DBFetcher(db_folder, db_name, table).fetch()


def deterfresh_manager(root, db_name):
    """Method to determine the manager that is mission or emotion manager and refresh it with using given database name and administration flag.

    Args:
        root (bool):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
    """

    if root:
        if db_name in ["predicted_missions", "missions"]:
            mission_manager.refresh_members()
        elif db_name == "emotions":
            emotion_manager.refresh_members()
    else:
        mission_manager.refresh_members()
