#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: r_sync
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for ability of T_System that about synchronization with remote storage.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.administration import is_admin

from t_system import r_synchronizer

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def sync(admin_id, in_use):
    """Method to start / stop remote storage synchronization.

    Args:
            admin_id (str):                 Admin privileges flag.
            in_use (bool):                  usage status flag.
    """

    try:
        if in_use:
            r_synchronizer.start_sync()
        else:
            r_synchronizer.stop_sync()

        return True
    except Exception as e:
        logger.error(e)
        return False


def is_sync_available(admin_id):
    """Method to check the synchronization's availability about networks connection.

    Args:
            admin_id (str):                 Admin privileges flag.
    """

    return r_synchronizer.is_sync_available()


def set_account_u_status(admin_id, service_name, account_name, in_use):
    """Method to set usage status of remote storage service's account.

    Args:
            admin_id (str):                 Admin privileges flag.
            service_name (str):             The name of the remote storage service.
            account_name (str):             Name of the website's account.
            in_use (str):                   usage status flag.
    """

    in_use = in_use in ["true", "True"]

    return r_synchronizer.activate_service_account(service_name, account_name)


def set_service_usage_status(admin_id, service_name, in_use):
    """Method to set usage status of remote storage service.

    Args:
            admin_id (str):                 Admin privileges flag.
            service_name (str):             The name of the remote storage service.
            in_use (str):                   usage status flag.
    """

    in_use = in_use in ["true", "True"]

    return r_synchronizer.set_service_usage_stat(service_name, in_use)


def set_auto_sync_status(admin_id, in_use):
    """Method to set automatically synchronization status of remote storage service.

    Args:
            admin_id (str):                 Admin privileges flag.
            in_use (str):                   usage status flag.
    """

    in_use = in_use in ["true", "True"]

    return r_synchronizer.change_status(in_use)


def get_auto_sync(admin_id):
    """Method to return status of the auto synchronization statement.

    Args:
        admin_id (str):                 Root privileges flag.
    """

    return r_synchronizer.is_sync_auto()


def create_account(admin_id, root, service_name, data):
    """Method to create new account for given storage service.

    Args:
            admin_id (str):                 Admin privileges flag.
            root (str):                     Root privileges activation flag.
            service_name (str):             The name of the remote storage service.
            data (dict):                    Account data structure.
    """

    try:
        result = r_synchronizer.set_service_account(service_name, data)

    except Exception as e:
        logger.error(e)
        result = False

    return result


def update_account(admin_id, root, service_name, data):
    """Method to update the account for given storage service.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            service_name (str):             The name of the remote storage service.
            data (dict):                    Account data structure.
    """

    return r_synchronizer.set_service_account(service_name, data)


def delete_account(admin_id, root, service_name, account_name):
    """Method to remove existing account that about given remote storage service.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            service_name (str):             The name of the remote storage service.
            account_name (str):             Name of the service's account.
    """

    return r_synchronizer.remove_service_account(service_name, account_name)


def get_services(admin_id, root):
    """Method to return existing remote storage services.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
    """
    result = []
    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        services = r_synchronizer.get_services()

        if services:
            for service in services:
                if service.name == "Dropbox":
                    result.append({"name": service.name, "to_be_used": service.to_be_used, "accounts": service.accounts})

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_service(admin_id, root, service_name):
    """Method to return existing service with given name.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            service_name (str):             The name of the remote storage service.
    """

    result = []

    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        services = r_synchronizer.get_websites(service_names=[service_name])

        if services:
            for service in services:
                if service.name == "Dropbox":
                    result.append({"name": service.name, "to_be_used": service.to_be_used, "accounts": service.accounts})

    except Exception as e:
        logger.error(e)
        result = []

    return result
