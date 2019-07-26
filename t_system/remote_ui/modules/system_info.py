#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for moving of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.system_info import *


def get_system_info(is_root):
    """The high-level method to get system info.

    Args:
        is_root (bool):                 Root privileges flag.
    """
    result = {}
    if is_root:
        result.update(get_ram_usage())
        result.update(get_cpu_usage())
        result.update(get_cpu_temperature())

    result.update(get_disk_usage(is_root))

    return result
