#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system.motion.arm.action import Position
from t_system import dot_t_system_dir
from t_system.motion.arm.action import predicted_actions_db


def create_position(is_root, data):
    """The high-level method to create new position.

    Args:
        is_root (bool):                 Root privileges flag.
        data (dict):                    Position data structure.
    """

    # table = get_db_table(is_root)

    position = Position(name=data['name'], cartesian_coords=data['cartesian_coords'], polar_coords=data['polar_coords'], root=is_root)

    try:
        result = True
        position_id = position.id
    except Exception:
        result = False
        position_id = None

    return result, position_id


def get_positions(is_root):
    """The high-level method to return existing positions.

    Args:
        is_root (bool):                 Root privileges flag.
    """
    try:
        table = get_db_table(is_root)

        result = table.all()  # result = positions

    except Exception as e:
        print(e)
        result = []

    return result


def get_position(is_root, position_id):
    """The high-level method to return existing position with given id.

    Args:
        is_root (bool):                 Root privileges flag.
        position_id (str):              The id of the position.
    """
    try:
        table = get_db_table(is_root)

        position = table.search((Query().id == position_id))

        if not position:
            result = []
        else:
            # result = [b.to_dict() for b in record]
            result = [position[0]]

    except Exception as e:
        print(e)
        result = []

    return result


def update_position(is_root, position_id, data):
    """The high-level method to update the position that is recorded in database with given parameters.

    Args:
        is_root (bool):                 Root privileges flag.
        position_id (str):              The id of the position.
        data (dict):                    Position data structure.
    """
    table = get_db_table(is_root)

    position = table.search((Query().id == position_id))

    if not position:
        result = False
    else:
        try:

            table.update({'name': data['name'], 'cartesian_coords': data['cartesian_coords'], 'polar_coords': data['polar_coords']}, Query().id == position_id)
            result = True
        except Exception:
            result = False

    return result


def delete_position(is_root, position_id):
    """The high-level method to remove existing position with given id.

    Args:
        is_root (bool):                 Root privileges flag.
        position_id (str):              The id of the position.
    """
    table = get_db_table(is_root)

    if table.search((Query().id == position_id)):
        table.remove((Query().id == position_id))

        result = True
    else:
        result = False

    return result


def get_db_table(is_root):
    """The low-level method to set work database by root.

    Args:
        is_root (bool):                 Root privileges flag.
    """
    if is_root:
        db_file = predicted_actions_db
    else:
        db_file = dot_t_system_dir + "/actions.json"

    db = TinyDB(db_file)
    return db.table("positions")
