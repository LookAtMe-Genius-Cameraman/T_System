#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: update
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's auto-update.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import update_manager


def get_status(admin_id, update_key):
    """Method to return existing positions.

    Args:
        admin_id (str):                 Root privileges flag.
        update_key (str):               Key of the requested status.
    """

    if update_key == "auto_update":
        status = update_manager.is_update_auto()
    elif update_key == "up_to_date":
        status = update_manager.update()
    else:
        status = None

    return status


def update_status(admin_id, data):
    """Method to update the position that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        data (dict):                    Update data structure.
    """
    update_manager.change_members(data["auto_update"])
    result = True
    return result
