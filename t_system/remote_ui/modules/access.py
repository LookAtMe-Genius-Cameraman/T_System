#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: access
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for accessing t_system from remote applications.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import request

from t_system import identifier
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class AccessManager:
    """Class to define a manager for accessing to the T_System.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.modules.access.AccessManager.get_stream`
        for the provide getting stream by calling iteratively the seer's current_frame member.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.modules.stream.StreamManager` class.
        """

        self.connection_count = 0

    def is_connectable(self):
        """Method to check active connection count of T_System. If there is device count that more than 1, returns False.
        """

        if self.connection_count < 1:
            return True

        return False

    def increase_cc(self):
        """Method to increase connection count when somebody connecting to the T_System device.
        """

        self.connection_count += 1

    def decrease_cc(self):
        """Method to decrease connection count when somebody disconnecting to the T_System device.
        """

        self.connection_count -= 1

    @staticmethod
    def check_private_id(private_id):
        """Method to verify incoming private id of T_System.

        Args:
            private_id (str):              Private id of identifier of T_System.
        """

        if private_id == identifier.private_id:
            return True
        return False

    @staticmethod
    def get_private_id_by(data):
        """Method to get private id of T_System if given data contains the public id.

        Args:
            data (dict):                    Access data structure.
        """

        if data["id"] in [identifier.public_id, identifier.name]:
            return identifier.private_id
        return False

    @staticmethod
    def shutdown_server():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
