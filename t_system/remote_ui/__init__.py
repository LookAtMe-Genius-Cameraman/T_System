#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of ImClass that contains the classes related to ImClasses about communicating with the HTML and JS via flask.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Flask, render_template, request, redirect, Response
from flask_session import Session

# from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Common pathname manipulations

import json
import os
import inspect

# from t_system.remote_ui.api.position import api_bp as position_api_bp
# from t_system.remote_ui.api.scenario import api_bp as scenario_api_bp
# from t_system.remote_ui.api.network import api_bp as network_api_bp
# from t_system.remote_ui.api.move import api_bp as move_api_bp
# from t_system.remote_ui.api.system_info import api_bp as system_info_api_bp
# from t_system import dot_t_system_dir
dot_t_system_dir = "/home/baybars/.t_system"

__version__ = '0.1.5'


REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class RemoteUI:
    """Class to define a flask handler to T_System communication ability with html and js.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.RemoteUI._set_app`
        for the using flask api to communications with html and js.

    """

    def __init__(self, args, template_folder, static_folder, vision=None):
        """Initialization method of :class:`t_system.remote_ui.RemoteUI` class.

            Args:
                args:       Command-line arguments.
                template_folder (str):  The folder of html templates.
                static_folder (str):    The folder of css and js files.
                vision:       	        Vision object from t_system.vision.Vision Class.

        """

        self.host = args["host"]
        self.port = args["port"]
        self.debug = args["debug"]

        self.remote_ui_dir = dot_t_system_dir + '/remote_ui'

        self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        Session(self.app)

        self._set_app()

        self.vision = vision

    def _set_app(self):
        """The low-level method to setting flask API.
        """

        # self.app.register_blueprint(position_api_bp)
        # self.app.register_blueprint(scenario_api_bp)
        # self.app.register_blueprint(network_api_bp)
        # self.app.register_blueprint(move_api_bp)
        # self.app.register_blueprint(system_info_api_bp)

        @self.app.route('/')
        def main():
            """The low-level method to routing main.html .
            """
            # db_json = json.dumps(self.db.all())
            db_json = json.dumps("something")
            return render_template('main.html', db_json=db_json)

        @self.app.route('/fulfill_command', methods=['POST'])
        def fulfill_command():
            """The low-level method to set working parameter of t_system.
            """
            cmd = request.form
            self.officiate(cmd)

            print(str(cmd))
            return str(cmd)

        @self.app.route('/try', methods=['POST'])
        def tryer():
            """The low-level method to set working parameter of t_system.
            """
            cmd = request.form

            print(str(cmd))
            return str(json.dumps({"vfdv": True}))  # it drops the resp.responseText.

    def run(self, host=None, port=None, debug=None):
        """The high-level method to running flask with given parameters.

        Args:
            host (string):          Host of the flask server.
            port (string):          Port of the flask server.
            debug (bool):           The debug flag.
        """

        if host is not None:
            self.host = host
        if port is not None:
            self.port = port
        if debug is not None:
            self.debug = debug

        self.app.run(host=self.host, port=self.port, debug=self.debug)

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def officiate(self, cmd):
        """The low-level method to fulfill commands those are coming from javascript ui.

        Args:
            cmd (dict):             container of incoming command
            port (string):          Port of the flask server.
            debug (bool):           The debug flag.
        """
        # cmd = {'status': False, 'for': '', 'reason': '', 'options': ''}

        status = cmd["status"]
        forr = cmd["for"]
        reason = cmd["reason"]
        options = cmd["options"]

        if status == "true":
            if forr == "live_stream":
                if reason == "start":
                    pass
                elif reason == "stop":
                    pass
            elif forr == "turn_joint":
                print(f"joint{reason} turned")
                # self.vision.arm.rotate_single_joint(reason, options)  # reason contains joint number and options contains delta angle.
            elif forr == "move_endpoint":
                print(f"axis{reason} moved")
                # self.vision.arm.move_endpoint(reason, options)  # reason contains axis name(x, y or z) and options contains distance as mm.

            elif forr == "configure":
                pass

        else:
            print("nope")

        pass


if __name__ == "__main__":

    REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    _template_folder = REMOTE_UI_PATH + "/www"
    _static_folder = _template_folder + "/static"

    app = RemoteUI(args={"host": "localhost", "port": "5000", "debug": True}, template_folder=_template_folder, static_folder=_static_folder)
    app.run(host="172.22.9.40", port="5000",  debug=True)
    # app.debug = True
