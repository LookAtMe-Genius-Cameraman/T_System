#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for moving of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.system_info import *
from t_system.accession import is_admin


def get_system_info(admin_id):
    """The high-level method to get system info.

    Args:
        admin_id (bool):                 Admin privileges flag.
    """
    result = {}
    if is_admin(admin_id):
        result.update(get_ram_usage())
        result.update(get_cpu_usage())
        result.update(get_cpu_temperature())

    result.update(get_disk_usage(admin_id))

    return result
