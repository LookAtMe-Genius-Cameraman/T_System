#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: identity
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for realizing identity process of T_System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.administration import is_admin

from t_system import identifier
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def get_identity_info(admin_id):
    """Method to get identity information of T_System.

    Args:
        admin_id (str):                 Root privileges flag.
    """
    identity_info = {"public_id": identifier.public_id, "private_id": None, "name": identifier.name}

    if admin_id:
        if is_admin(admin_id):
            identity_info["private_id"] = identifier.private_id

    return identity_info


def update_identity(admin_id, cause, data):
    """Method to identity information of T_System as given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        cause (str):                    Key that will be change.
        data (dict):                    Identity data structure.
    """
    result = True

    root = is_admin(admin_id)

    if cause:
        if root:
            if cause == "public_id":
                identifier.change_keys(public_id=data["public_id"])
            elif cause == "private_id":
                identifier.change_keys(private_id=data["private_id"])
        if cause == "name":
            identifier.change_keys(name=data["name"])
        else:
            result = False
    else:
        if root:
            result = identifier.change_keys(data["public_id"], data["private_id"], data["name"])
        else:
            result = identifier.change_keys(name=data["name"])

    return result
