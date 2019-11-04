#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for moving of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.foundation import *
from t_system.administration import is_admin


def get_system_info(admin_id):
    """Method to get system info.

    Args:
        admin_id (str):                 Admin privileges flag.
    """
    root = is_admin(admin_id)

    result = {}

    result.update(get_ram_usage(root))
    result.update(get_cpu_usage(root))
    result.update(get_cpu_temperature(root))
    result.update(get_disk_usage(root))
    result.update(get_versions(root))

    return result
