# -*- coding: utf-8 -*-

"""
.. module:: test_remote_ui
    :platform: Unix
    :synopsis: tests for the remote_ui submodule.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import requests
import os  # Miscellaneous operating system interfaces
import inspect  # Inspect live objects

from flask import Flask
from flask_testing import LiveServerTestCase, TestCase

from t_system.remote_ui import RemoteUI

T_SYSTEM_PATH = f'{os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))}/..'
REMOTE_UI_PATH = f'{T_SYSTEM_PATH}/remote_ui'


class TestRemoteUILive(LiveServerTestCase):
    """Class to define a flask tester to T_System communication ability with html and js.

        This class provides necessary initiations and a functions named start with `test` keyword.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.tests.test_remote_ui.TestRemoteUI` class.
        """
        super().__init__()

    def create_app(self):
        """Function to create a Flask instance for testing.

        Returns:
            Flask:  An Flask object.
        """

        template_folder = T_SYSTEM_PATH + "/remote_ui/www"
        static_folder = template_folder + "/static"

        remote_ui = RemoteUI(args={"host": "localhost", "port": "5000", "debug": True, "mode": "testing"}, template_folder=template_folder, static_folder=static_folder)

        return remote_ui.app

    def test_server_is_up_and_running(self):
        try:
            response = requests.get(self.get_server_url())
            self.assertEqual(response.status_code, 200)
        except requests.ConnectionError:
            pass


class TestRemoteUI(TestCase):
    """Class to define a flask tester to T_System communication ability with html and js.

        This class provides necessary initiations and a functions named start with `test` keyword.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.tests.test_remote_ui.TestRemoteUI` class.
        """
        super().__init__()

    def create_app(self):
        """Function to create a Flask instance for testing.

        Returns:
            Flask:  An Flask object.
        """

        template_folder = T_SYSTEM_PATH + "/remote_ui/www"
        static_folder = template_folder + "/static"

        remote_ui = RemoteUI(args={"host": "localhost", "port": "5000", "debug": True, "mode": "testing"}, template_folder=template_folder, static_folder=static_folder)

        return remote_ui.app

    def test_position(self):
        response = self.client.post("/api/position", {"name": "position_name", "cartesian_coords": [30, 25, 42], "polar_coords": [1.5, 1.02, 0.5]})
        response = self.client.get("/ajax/")  # THIS WORKS WITH TestCase.
        self.assertEquals(response.json, dict(success=True))
