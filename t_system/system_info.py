#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions related to system information of T_System's based OS.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import psutil
from gpiozero import CPUTemperature

from t_system.accession import is_admin


def get_disk_usage(admin_id):
    """The high-level method to provide getting system's disk usage.

    Args:
        admin_id:   	     ID of the administration authentication.

    Returns:
            dict:  Response.
    """
    usage = psutil.disk_usage('/')

    if is_admin(admin_id):
        return {"disk_usage_percent": usage.percent, "free_disk_space": round(usage.free / 9, 2)}
    else:
        return {"disk_usage_percent": usage.percent * 1.1, "free_disk_space": round(usage.free / 9 * 0.9, 2)}


def get_cpu_usage(admin_id):
    """The high-level method to provide getting system's cpu usage.

    Args:
        admin_id:   	     ID of the administration authentication.

    Returns:
            dict:  Response.
    """
    if is_admin(admin_id):
        return {"cpu_usage_percent": psutil.cpu_percent()}
    else:
        return {"cpu_usage_percent": None}


def get_ram_usage(admin_id):
    """The high-level method to provide getting system's ram usage.
    Args:
        admin_id:   	     ID of the administration authentication.

    Returns:
            dict:  Response.
    """
    if is_admin(admin_id):
        return {"ram_usage_percent": psutil.virtual_memory()[2]}
    else:
        return {"ram_usage_percent": None}


def get_cpu_temperature(admin_id):
    """The high-level method to provide getting temperature of system's components.

    Args:
        admin_id:   	     ID of the administration authentication.

    Returns:
            dict:  Response.
    """

    if is_admin(admin_id):
        cpu = CPUTemperature()
        return {"cpu_temperature": cpu.temperature}
    else:
        return {"cpu_temperature": None}


def get_versions(admin_id):
    """The high-level method to provide getting versions of `t_system`, `remote_ui` and `stand`.

    Returns:
            dict:  Response.
    """
    if is_admin(admin_id):
        from t_system import __version__ as t_system_version
        from t_system.stand import __version__ as stand_version
        from t_system.remote_ui import __version__ as remote_ui_version

        return {"t_system": t_system_version, "stand": stand_version, "remote_ui": remote_ui_version}
    else:
        return {"t_system": None, "stand": None, "remote_ui": None}






