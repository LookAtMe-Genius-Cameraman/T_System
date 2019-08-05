# -*- coding: utf-8 -*-

"""
.. module:: test_system_info
    :platform: Unix
    :synopsis: tests for the system_info submodule.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.system_info import *

from gpiozero import CPUTemperature

import psutil
import pytest


disk_usage = psutil.disk_usage('/')
cpu = CPUTemperature()


def test_get_disk_usage():
    assert get_disk_usage(False) == {"disk_usage_percent": disk_usage.percent, "free_disk_space": round(disk_usage.free / 9, 2)}


def test_get_cpu_usage():
    assert get_cpu_usage() == {"cpu_usage_percent": psutil.cpu_percent()}


def test_get_ram_usage():
    assert get_ram_usage() == {"ram_usage_percent": psutil.virtual_memory()[2]}


def test_get_cpu_temperature():
    assert get_cpu_temperature() == {"cpu_temperature": cpu.temperature}
