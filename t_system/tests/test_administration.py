# -*- coding: utf-8 -*-

"""
.. module:: test_administration
    :platform: Unix
    :synopsis: tests for the administration submodule.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from os.path import expanduser  # Common pathname manipulations

from t_system.administration import Administrator

import os  # Miscellaneous operating system interfaces
import pytest


home = expanduser("~")
dot_t_system_dir = home + "/.t_system"

if os.path.exists(dot_t_system_dir + '/db.json'):
    os.remove(dot_t_system_dir + '/db.json')  # This is where we store the database; /home/USERNAME/.t_system/db.json


@pytest.fixture
def administrator():
    """Returns a :class:`t_system.administration.Administrator` instance."""

    return Administrator()


def test_administrator_change_keys(administrator):
    administrator.change_keys("test_ssid", "test_password")
    assert administrator.ssid_hash == "ee79e4fb679aa1429973b139e51d8ede2fa934302548a02f19054d13548876e3"
    assert administrator.password_hash == "a196d5d19f01b45e35da304d14c5d053d8ea8c18eb489f8ee5603ba35a8dd477"
    assert administrator.private_key == "4a9635a008c0ef2a1434553533b4fefab49112dd0f70417537e126e63149d163"
