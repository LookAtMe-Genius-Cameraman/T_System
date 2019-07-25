#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system.motion.arm.action import Scenario
from t_system import dot_t_system_dir
from t_system.motion.arm.action import predicted_actions_db


def create_scenario(is_root, data):
    """The high-level method to create new scenario.

    Args:
        is_root (bool):                 Root privileges flag.
        data (dict):                    Scenario data structure.
    """

    # table = get_db_table(is_root)

    scenario = Scenario(name=data['name'], root=is_root)

    try:
        result = True
        scenario_id = scenario.id
    except Exception:
        result = False
        scenario_id = None

    return result, scenario_id


def get_scenarios(is_root):
    """The high-level method to return existing scenarios.

    Args:
        is_root (bool):                 Root privileges flag.
    """
    try:
        table = get_db_table(is_root)

        result = table.all()  # result = scenarios

    except Exception as e:
        print(e)
        result = []

    return result


def get_scenario(is_root, scenario_id):
    """The high-level method to return existing scenario with given id.

    Args:
        is_root (bool):                 Root privileges flag.
        scenario_id (str):              The id of the scenario.
    """
    try:
        table = get_db_table(is_root)

        scenario = table.search((Query().id == scenario_id))

        if not scenario:
            result = []
        else:
            # result = [b.to_dict() for b in record]
            result = [scenario[0]]

    except Exception as e:
        print(e)
        result = []

    return result


def update_scenario(is_root, scenario_id, data):
    """The high-level method to update the scenario that is recorded in database with given parameters.

    Args:
        is_root (bool):                 Root privileges flag.
        scenario_id (str):              The id of the scenario.
        data (dict):                    Position data structure.
    """
    table = get_db_table(is_root)

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


def delete_scenario(is_root, scenario_id):
    """The high-level method to remove existing position with given id.

    Args:
        is_root (bool):                 Root privileges flag.
        scenario_id (str):              The id of the position.
    """
    table = get_db_table(is_root)

    if table.search((Query().id == scenario_id)):
        table.remove((Query().id == scenario_id))

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
    return db.table("scenarios")
