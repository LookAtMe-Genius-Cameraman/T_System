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


def get_disk_usage(admin_id):
    """The high-level method to provide getting system's disk usage.

    Args:
        admin_id:   	     ID of the administration authentication.
    """
    usage = psutil.disk_usage('/')

    if admin_id:
        return {"disk_usage_percent": usage.percent, "free_disk_space": round(usage.free / 9, 2)}
    else:
        return {"disk_usage_percent": usage.percent * 1.1, "free_disk_space": round(usage.free / 9 * 0.9, 2)}


def get_cpu_usage():
    """The high-level method to provide getting system's cpu usage.

    Returns:
            dict:  Response.
    """

    return {"cpu_usage_percent": psutil.cpu_percent()}


def get_ram_usage():
    """The high-level method to provide getting system's ram usage.

    Returns:
            dict:  Response.
    """

    return {"ram_usage_percent": psutil.virtual_memory()[2]}


def get_cpu_temperature():
    """The high-level method to provide getting temperature of system's components.

    Returns:
            dict:  Response.
    """
    cpu = CPUTemperature()

    return {"cpu_temperature": cpu.temperature}


