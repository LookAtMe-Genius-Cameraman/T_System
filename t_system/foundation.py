#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: system_info
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions related to system information of T_System's based OS.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import time  # Time access and conversions
import subprocess  # Subprocess managements

import psutil

from gpiozero import CPUTemperature

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def get_disk_usage(is_admin):
    """Method to provide getting system's disk usage.

    Args:
        is_admin (bool):     Root privileges flag.

    Returns:
        dict:  Response.
    """
    usage = psutil.disk_usage('/')

    if is_admin:
        return {"disk_usage_percent": round(usage.percent, 2), "free_disk_space": round(usage.free / 10 ** 9, 2)}
    else:
        return {"disk_usage_percent": round(usage.percent * 1.1, 2), "free_disk_space": round(usage.free / 10 ** 9 * 0.9, 2)}


def get_cpu_usage(is_admin):
    """Method to provide getting system's cpu usage.

    Args:
        is_admin (bool):     Root privileges flag.

    Returns:
            dict:  Response.
    """
    if is_admin:
        return {"cpu_usage_percent": psutil.cpu_percent()}
    else:
        return {"cpu_usage_percent": None}


def get_ram_usage(is_admin):
    """Method to provide getting system's ram usage.
    Args:
        is_admin (bool):     Root privileges flag.

    Returns:
            dict:  Response.
    """
    if is_admin:
        return {"ram_usage_percent": psutil.virtual_memory()[2]}
    else:
        return {"ram_usage_percent": None}


def get_cpu_temperature(is_admin):
    """Method to provide getting temperature of system's components.

    Args:
        is_admin (bool):     Root privileges flag.

    Returns:
            dict:  Response.
    """

    if is_admin:
        cpu = CPUTemperature()
        return {"cpu_temperature": cpu.temperature}
    else:
        return {"cpu_temperature": None}


def get_versions(is_admin):
    """Method to provide getting versions of `t_system`, `remote_ui` and `stand`.

    Args:
        is_admin (bool):     Root privileges flag.

    Returns:
            dict:  Response.
    """
    if is_admin:
        from t_system import __version__ as t_system_version
        from t_system.stand import __version__ as stand_version
        from t_system.remote_ui import __version__ as remote_ui_version

        return {"versions": {"t_system": t_system_version, "stand": stand_version, "remote_ui": remote_ui_version}}
    else:
        return {"versions": {"t_system": None, "stand": None, "remote_ui": None}}


def shutdown(s_time=0, force=False):
    """Method to provide power off the sub-system of T_System.

    Args:
        s_time:   	         Shutting down time.
        force:   	         Force shutdown flag.

    Returns:
            dict:  Response.
    """

    result = True
    try:
        time.sleep(s_time)
        subprocess.call("shutdown -h now", shell=True)
    except Exception as e:
        logger.warning(f'Shutdown error: {e}')
        result = False

    return result


def restart(r_time=0, force=False):
    """Method to provide reboot the sub-system of T_System.

    Args:
        r_time:   	         Shutting down time.
        force:   	         Force shutdown flag.

    Returns:
            dict:  Response.
    """

    result = True
    try:
        time.sleep(r_time)
        subprocess.call("reboot -h now", shell=True)
    except Exception as e:
        logger.warning(f'Restart error: {e}')
        result = False

    return result
