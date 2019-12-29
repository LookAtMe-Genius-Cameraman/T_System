#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: log
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for T_System log management.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.administration import is_admin

from t_system import log_manager


def get_logfile(admin_id):
    """Method to get logfile of log_manager object.

    Args:
            admin_id (str):                 Admin privileges flag.
    """

    if is_admin(admin_id):
        return log_manager.get_logfile()

    return False, False


def clear_logs(admin_id):
    """Method to clear logs that taken from log_manager object.

    Args:
            admin_id (str):                 Admin privileges flag.
    """

    if is_admin(admin_id):
        return log_manager.clear_logs()

    return False
