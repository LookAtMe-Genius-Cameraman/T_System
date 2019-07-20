#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of ImClass that contains the classes related to ImClasses about communicating with the HTML and JS via flask.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Flask, render_template, request, redirect, Response
# from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Common pathname manipulations

import json
import os
import inspect

REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class RemoteUI:
    """Class to define a flask handler to T_System communication ability with html and js.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.RemoteUI._set_app`
        for the using flask api to communications with html and js.

    """

    def __init__(self, template_folder, static_folder, vision=None):
        """Initialization method of :class:`t_system.remote_ui.RemoteUI` class.

            Args:
                template_folder (str):  The folder of html templates.
                static_folder (str):    The folder of css and js files.
                vision:       	        Vision object from t_system.vision.Vision Class.

        """
        home = expanduser("~")
        dot_t_system_dir = home + "/.t_system"
        self.remote_ui_dir = dot_t_system_dir + '/remote_ui'

        self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        self._set_app()

        self.vision = vision

    def _set_app(self):
        """The low-level method to setting flask API.
        """
        @self.app.route('/')
        def main():
            """The low-level method to routing main.html .
            """
            # db_json = json.dumps(self.db.all())
            db_json = json.dumps("something")
            return render_template('main.html', db_json=db_json)

        @self.app.route('/set_running_params', methods=['POST'])
        def set_running_params():
            """The low-level method to set working parameter of t_system.
            """
            param_data = request.form

            print(str(param_data))
            return str(param_data)

        @self.app.route('/start_live_stream', methods=['POST'])
        def start_live_stream():
            """The low-level method to start live video stream for previewing or record monitoring.
            """
            param_data = request.form

            print(str(param_data))
            return str(param_data)

        @self.app.route('/move_arm', methods=['POST'])
        def move_arm():
            """The low-level method to move the arm by taking ways and types.
            """
            param_data = request.form

            print(str(param_data))
            return str(param_data)

    def run(self, host='localhost', port=5000, debug=False):
        """The high-level method to running flask with given parameters.

        Args:
            host (string):          Host of the flask server.
            port (string):          Port of the flask server.
            debug (bool):           The debug flag.
        """
        self.app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":

    REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    _template_folder = REMOTE_UI_PATH + "/www"
    _static_folder = _template_folder + "/static"

    app = RemoteUI(template_folder=_template_folder, static_folder=_static_folder)
    app.run(debug=True)
    # app.debug = True
