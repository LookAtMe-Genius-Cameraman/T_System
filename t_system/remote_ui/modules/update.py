#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: update
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's auto-update.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import update_manager

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def get_status(admin_id, update_key):
    """Method to return status of the self-update statement.

    Args:
        admin_id (str):                 Root privileges flag.
        update_key (str):               Key of the requested status.
    """

    if update_key == "auto_update":
        status = update_manager.is_update_auto()
    else:
        status = None

    return status


def update_status(admin_id, data):
    """Method to update the self-update statement.

    Args:
        admin_id (str):                 Root privileges flag.
        data (dict):                    Update data structure.
    """
    update_manager.change_members(data["auto_update"])
    result = True
    return result


def up_to_date(admin_id):
    """Method to trig update processes of T_System itself.

    Args:
        admin_id (str):                 Root privileges flag.
    """

    return update_manager.update()
