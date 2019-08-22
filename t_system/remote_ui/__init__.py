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

import json
import os
import inspect

from t_system.remote_ui.api.position import api_bp as position_api_bp
from t_system.remote_ui.api.scenario import api_bp as scenario_api_bp
from t_system.remote_ui.api.network import api_bp as network_api_bp
from t_system.remote_ui.api.move import api_bp as move_api_bp
from t_system.remote_ui.api.system_info import api_bp as system_info_api_bp
from t_system.remote_ui.api.face_encoding import api_bp as face_encoding_api_bp
from t_system.remote_ui.api.stream import api_bp as stream_api_bp
from t_system import T_SYSTEM_PATH, dot_t_system_dir
# dot_t_system_dir = "/home/baybars/.t_system"

__version__ = '0.3.3'


REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class RemoteUI:
    """Class to define a flask handler to T_System communication ability with html and js.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.RemoteUI._set_app`
        for the using flask api to communications with html and js.

    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.remote_ui.RemoteUI` class.

            Args:
                args:       Command-line arguments.
        """

        self.host = args["host"]
        self.port = args["port"]
        self.debug = args["debug"]

        template_folder = T_SYSTEM_PATH + "/remote_ui/www"
        static_folder = template_folder + "/static"
        self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

        self.remote_ui_dir = dot_t_system_dir + '/remote_ui'

        config_file = f'{REMOTE_UI_PATH}/config/{args["environment"]}.cfg'
        self.app.config.from_pyfile(config_file)

        Session(self.app)

        self._set_app()

    def _set_app(self):
        """The low-level method to setting flask API.
        """

        self.app.register_blueprint(position_api_bp)
        self.app.register_blueprint(scenario_api_bp)
        self.app.register_blueprint(network_api_bp)
        self.app.register_blueprint(move_api_bp)
        self.app.register_blueprint(system_info_api_bp)
        self.app.register_blueprint(face_encoding_api_bp)
        self.app.register_blueprint(stream_api_bp)

        @self.app.route('/')
        def main():
            """The low-level method to routing main.html .
            """
            # db_json = json.dumps(self.db.all())
            db_json = json.dumps("something")
            return render_template('main.html', db_json=db_json)

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


if __name__ == "__main__":

    REMOTE_UI_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    _template_folder = REMOTE_UI_PATH + "/www"
    _static_folder = _template_folder + "/static"

    app = RemoteUI(args={"host": "localhost", "port": "5000", "debug": True, "environment": "development"}, template_folder=_template_folder, static_folder=_static_folder)
    app.run(host="172.22.9.40", port="5000",  debug=True)
    # app.debug = True
