#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of T_System that contains the initial module imports and global variables.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os  # Miscellaneous operating system interfaces
import inspect  # Inspect live objects

from os.path import expanduser  # Common pathname manipulations

log_manager = None
seer = None
augmenter = None
stand_ui = None
administrator = None
update_manager = None

T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

home = expanduser("~")
dot_t_system_dir = home + "/.t_system"

__author__ = 'Cem Baybars GÜÇLÜ'
__email__ = 'cem.baybars@gmail.com'
__version__ = '0.9-alpha2.21'
