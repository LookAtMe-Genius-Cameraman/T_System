#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: wifi
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's wifi connections.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher
from t_system import dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def change_nc_activity(admin_id, activity):
    """Method to change status of NetworkConnector.

    Args:
        admin_id (str):                 Admin privileges flag.
        activity (bool):                Activity status of network_connector of stand_ui.
    """

    result = True

    try:
        from t_system import stand_ui
        stand_ui.network_connector.change_status(activity)
    except Exception as e:
        logger.error(e)
        result = False

    return result


def get_nc_activity(admin_id):
    """Method to get status of NetworkConnector.

    Args:
        admin_id (str):                 Admin privileges flag.
    """

    from t_system import stand_ui

    return stand_ui.network_connector.activity


def create_network(admin_id, data):
    """Method to create new network.

    Args:
        admin_id (str):                 Admin privileges flag.
        data (dict):                    Network data structure.
    """
    try:
        from t_system import stand_ui
        result, admin_id = stand_ui.network_connector.add_network(data["ssid"], data["password"])
    except Exception as e:
        logger.error(e)
        result = False

    return result, admin_id


def get_networks(admin_id):
    """Method to return existing networks.

    Args:
        admin_id (str):                 Admin privileges flag.
    """
    try:
        table = get_db_table()
        result = table.all()  # result = networks

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_network(admin_id, network_ssid):
    """Method to return existing network with given id.

    Args:
        admin_id (str):                 Admin privileges flag.
        network_ssid (str):             The ssid of the network.
    """
    try:
        table = get_db_table()

        network = table.search((Query().ssid == network_ssid))

        if not network:
            result = []
        else:
            result = [network[0]]

    except Exception as e:
        logger.error(e)
        result = []

    return result


def update_network(admin_id, ssid, data):
    """Method to update the network that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Admin privileges flag.
        ssid:       	                The ssid of the network.
        data (dict):                    Network data structure.
    """
    table = get_db_table()
    network = table.search((Query().ssid == ssid))

    if not network:
        result = False
    else:
        try:
            table.update({'ssid': data["ssid"], 'password': data["password"]}, Query().ssid == ssid)
            result = True
        except Exception:
            result = False

    return result


def delete_network(admin_id, ssid):
    """Method to remove existing network with given id.

    Args:
        admin_id (str):                 Admin privileges flag.
        ssid (str):                     The ssid of the network.
    """
    table = get_db_table()

    if table.search((Query().id == ssid)):
        table.remove((Query().id == ssid))

        result = True
    else:
        result = False

    return result


def get_db_table():
    """Method to get work database.
    """

    db_folder = f'{dot_t_system_dir}/network'
    return DBFetcher(db_folder, "db", "login").fetch()
