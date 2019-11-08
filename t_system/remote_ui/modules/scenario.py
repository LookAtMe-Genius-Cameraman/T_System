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
from t_system.motion.action import Scenario
from t_system.motion.action import Position
from t_system.administration import is_admin
from t_system.remote_ui.modules.position import deterfresh_manager

from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_scenario(admin_id, root, db_name, data):
    """Method to create new scenario.

    Args:
        admin_id (str):                 Admin privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        data (dict):                    Scenario data structure.
    """
    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    scenario = Scenario(name=data['name'], root=root, db_name=db_name)

    try:
        positions = []
        for position in data['positions']:
            positions.append(Position(name=position["name"], cartesian_coords=position["cartesian_coords"],
                                      polar_params=position["polar_params"], root=root, db_name=db_name, is_for_scenario=True))
        scenario.add_positions(positions)
        scenario_id = scenario.id

        deterfresh_manager(root, db_name)
        result = True
    except Exception:
        result = False
        scenario_id = None

    return result, scenario_id


def get_scenarios(admin_id, root, db_name):
    """Method to return existing scenarios.

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

        result = table.all()  # result = scenarios

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_scenario(admin_id, root, db_name, scenario_id):
    """Method to return existing scenario with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        scenario_id (str):              The id of the scenario.
    """
    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        table = get_db_table(root, db_name)

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


def update_scenario(admin_id, root, db_name, scenario_id, data):
    """Method to update the scenario that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                    Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        scenario_id (str):              The id of the scenario.
        data (dict):                    Position data structure.
    """
    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    table = get_db_table(root, db_name)

    scenario = table.search((Query().id == scenario_id))

    if not scenario:
        result = False
    else:
        Scenario(data['name'], scenario_id, root, db_name).update_all_positions(
            [Position(name=position["name"],
                      cartesian_coords=position["cartesian_coords"],
                      polar_params=position["polar_params"],
                      root=root,
                      db_name=db_name,
                      is_for_scenario=True) for position in data['positions']])
        deterfresh_manager(root, db_name)
        result = True

    return result


def delete_scenario(admin_id, root, db_name, scenario_id):
    """Method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        root (str):                     Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        scenario_id (str):              The id of the position.
    """

    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    table = get_db_table(root, db_name)

    if table.search((Query().id == scenario_id)):
        table.remove((Query().id == scenario_id))
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
    table = "scenarios"
    if root:
        db_folder = f'{T_SYSTEM_PATH}/motion/action'
        return DBFetcher(db_folder, db_name, table).fetch()
    else:
        db_folder = dot_t_system_dir
        db_name = 'missions'
        return DBFetcher(db_folder, db_name, table).fetch()
