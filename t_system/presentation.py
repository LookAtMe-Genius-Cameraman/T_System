#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: presentation
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's presenting itself to user ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os  # Miscellaneous operating system interfaces
import shutil  # High-level file operations
import pkg_resources

from subprocess import call  # Subprocess managements


def startup_banner():
    """The top-level method to create startup banner of T_System itself.
    """

    (columns, lines) = shutil.get_terminal_size()

    call(f'figlet -f smslant \'T_System\' | boxes -d diamonds -a hcvc -p h8 | /usr/games/lolcat -a -d 1', shell=True)  # covers 65 columns.

    call(f'echo {int(columns * 0.85) * "_"} | /usr/games/lolcat', shell=True)
    print("\n")


def versions_banner():
    """The top-level method to draw banner for showing versions of T_System.
    """

    import t_system.__init__

    if not os.path.exists(t_system.dot_t_system_dir):
        os.mkdir(t_system.dot_t_system_dir)

    from t_system.logging import LogManager

    t_system.log_manager = LogManager(args={"verbose": False, "environment": None})

    from t_system.stand import __version__ as stand_version
    from t_system.remote_ui import __version__ as remote_ui_version

    t_system_version = pkg_resources.get_distribution("t_system").version

    versions = f't_system: {t_system_version}\nremote_ui: {remote_ui_version}\nstand: {stand_version}'
    call(f'figlet -f term \'{versions}\' | boxes -d spring -a hcvc -p h8 | /usr/games/lolcat -a -d 1', shell=True)
