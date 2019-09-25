#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: move
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for moving of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import arm


def move_arm(admin_id, move_id, data):
    """Method to move T_System's arm.

    Args:
        admin_id (str):                Admin privileges flag.
        data (dict):                    Move data structure.
    """
    result = True

    if data["type"] == "joint":
        arm.rotate_single_joint(int(data["id"]), data["quantity"])
    elif data["type"] == "axis":
        arm.move_endpoint(data["id"], data["quantity"])
    else:
        result = False

    return result


def get_arm_current_position(admin_id):
    """Method to get coordinates of T_System's arm current position as polar and cartesian.

    Args:
        admin_id (str):                Admin privileges flag.
    """

    return arm.get_current_positions()


def get_arm_joint_count(admin_id):
    """Method to get joint count of the Robotic Arm for handling expansion of it.

    Args:
        admin_id (str):                Admin privileges flag.
    """

    return len(arm.joints) - 1

