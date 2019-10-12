#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: access
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for accessing t_system from remote applications.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import identifier
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def check_private_id(private_id):
    """Method to verify incoming private id of T_System.

    Args:
        private_id (str):              Private id of identifier of T_System.
    """

    if private_id == identifier.private_id:
        return True
    return False


def get_private_id_by(data):
    """Method to get private id of T_System if given data contains the public id.

    Args:
        data (dict):                    Access data structure.
    """

    if data["id"] == identifier.public_id:
        return identifier.private_id
    return False
