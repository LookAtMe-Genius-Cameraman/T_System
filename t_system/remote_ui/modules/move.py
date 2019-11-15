#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: move
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for moving of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.administration import is_admin

from t_system import arm
from t_system import seer
from t_system import mission_manager, emotion_manager
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def set_arm(admin_id, expand):
    """Method to set expansion of T_System's arm.

    Args:
        admin_id (str):                Admin privileges flag.
        expand (str):                  Expansion flag of the arm.
    """

    if expand in ["true", "True"]:
        if not arm.is_expanded():
            expansion_angles = seer.reload_target_locker(arm_expansion=True)
            arm.expand(current_angles=expansion_angles)
    else:
        if arm.is_expanded():
            locker_angles = arm.revert_the_expand()
            seer.reload_target_locker(arm_expansion=False, current_angles=locker_angles)


def move_arm(admin_id, move_id, data):
    """Method to move T_System's arm.

    Args:
        admin_id (str):                Admin privileges flag.
        data (dict):                   Move data structure.
    """
    result = True

    if data["type"] == "joint":
        arm.rotate_single_joint(int(data["id"]), data["quantity"])
    elif data["type"] == "axis":
        arm.move_endpoint(data["id"], data["quantity"])
    else:
        result = False

    return result


def move_arm_by(admin_id, root, db_name, action, a_type):
    """Method to get coordinates of T_System's arm current position as polar and cartesian.

    Args:
        admin_id (str):                Admin privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                 Name of the registered Database. It uses if administration privileges activated.
        action (str):                  Name of the position or scenario that will simulated.
        a_type (str):                  The type of the action. Position or Scenario
    """

    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    if db_name == "emotions":
        emotion_manager.make_feel(action, a_type)
    elif db_name in ["missions", "predicted_missions"]:
        mission_manager.execute(action, a_type, root)


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

