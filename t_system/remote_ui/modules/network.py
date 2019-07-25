#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: wifi
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's wifi connections.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from elevate import elevate

from t_system.accession import NetworkManager
from t_system import dot_t_system_dir


def create_network(is_root, data):
    """The high-level method to create new scenario.

    Args:
        is_root (bool):                 Root privileges flag.
        data (dict):                    Network data structure.
    """
    try:
        with elevate(show_console=False, graphical=False):
            network_manager = NetworkManager()
            result = True
            network_manager.add_network(data["ssid"], data["password"])
    except Exception:
        result = False

    return result


def get_networks(is_root):
    """The high-level method to return existing scenarios.

    Args:
        is_root (bool):                 Root privileges flag.
    """
    try:
        table = get_db_table()
        result = table.all()  # result = networks

    except Exception as e:
        print(e)
        result = []

    return result


def get_network(is_root, network_ssid):
    """The high-level method to return existing network with given id.

    Args:
        is_root (bool):                 Root privileges flag.
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
        print(e)
        result = []

    return result


def update_network(is_root, ssid, data):
    """The high-level method to update the scenario that is recorded in database with given parameters.

    Args:
        is_root (bool):                 Root privileges flag.
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


def delete_network(is_root, ssid):
    """The high-level method to remove existing position with given id.

    Args:
        is_root (bool):                 Root privileges flag.
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
    """The low-level method to get work database.
    """

    db_file = dot_t_system_dir + "/network/db.json"
    db = TinyDB(db_file)

    return db.table("login")
