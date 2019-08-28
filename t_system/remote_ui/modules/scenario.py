#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system.administration import is_admin
from t_system.motion.action.__init__ import Scenario

from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_scenario(admin_id, data):
    """The high-level method to create new scenario.

    Args:
        admin_id (str):                 Admin privileges flag.
        data (dict):                    Scenario data structure.
    """

    # table = get_db_table(is_admin(admin_id))

    scenario = Scenario(name=data['name'], root=is_admin(admin_id))

    try:
        result = True
        scenario_id = scenario.id
    except Exception:
        result = False
        scenario_id = None

    return result, scenario_id


def get_scenarios(admin_id):
    """The high-level method to return existing scenarios.

    Args:
        admin_id (str):                 Root privileges flag.
    """
    try:
        table = get_db_table(is_admin(admin_id))

        result = table.all()  # result = scenarios

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_scenario(admin_id, scenario_id):
    """The high-level method to return existing scenario with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        scenario_id (str):              The id of the scenario.
    """
    try:
        table = get_db_table(is_admin(admin_id))

        scenario = table.search((Query().id == scenario_id))

        if not scenario:
            result = []
        else:
            # result = [b.to_dict() for b in record]
            result = [scenario[0]]

    except Exception as e:
        logger.error(e)
        result = []

    return result


def update_scenario(admin_id, scenario_id, data):
    """The high-level method to update the scenario that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        scenario_id (str):              The id of the scenario.
        data (dict):                    Position data structure.
    """
    table = get_db_table(is_admin(admin_id))

    scenario = table.search((Query().id == scenario_id))

    if not scenario:
        result = False
    else:
        try:

            table.update({'name': data['name'], 'positions': data['positions']}, Query().id == scenario_id)
            result = True
        except Exception:
            result = False

    return result


def delete_scenario(admin_id, scenario_id):
    """The high-level method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        scenario_id (str):              The id of the position.
    """
    table = get_db_table(is_admin(admin_id))

    if table.search((Query().id == scenario_id)):
        table.remove((Query().id == scenario_id))

        result = True
    else:
        result = False

    return result


def get_db_table(is_admin):
    """The low-level method to set work database by root.

    Args:
        is_admin (bool):                 Root privileges flag.
    """
    if is_admin:
        db_file = f'{T_SYSTEM_PATH}/motion/action/predicted_actions.json'
    else:
        db_file = dot_t_system_dir + "/actions.json"

    db = TinyDB(db_file)
    return db.table("scenarios")
