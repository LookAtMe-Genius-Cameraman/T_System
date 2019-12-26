#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __main__
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System about communicating with the HTML and JS via flask.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from flask import Flask, render_template, request, redirect, Response
from flask_session import Session

from t_system.remote_ui.api.access import api_bp as access_api_bp
from t_system.remote_ui.api.face_encoding import api_bp as face_encoding_api_bp
from t_system.remote_ui.api.identity import api_bp as identity_api_bp
from t_system.remote_ui.api.job import api_bp as job_api_bp
from t_system.remote_ui.api.live_stream import api_bp as live_stream_api_bp
from t_system.remote_ui.api.move import api_bp as move_api_bp
from t_system.remote_ui.api.network import api_bp as network_api_bp
from t_system.remote_ui.api.position import api_bp as position_api_bp
from t_system.remote_ui.api.r_sync import api_bp as r_sync_api_bp
from t_system.remote_ui.api.record import api_bp as record_api_bp
from t_system.remote_ui.api.scenario import api_bp as scenario_api_bp
from t_system.remote_ui.api.stream import api_bp as stream_api_bp
from t_system.remote_ui.api.system_info import api_bp as system_info_api_bp
from t_system.remote_ui.api.update import api_bp as update_api_bp

from t_system import T_SYSTEM_PATH, dot_t_system_dir


class RemoteUI:
    """Class to define a flask handler to T_System communication ability with html and js.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.RemoteUI.__set_app`
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

        template_folder = f'{T_SYSTEM_PATH}/remote_ui/www'
        static_folder = f'{template_folder}/static'
        self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

        self.remote_ui_dir = f'{dot_t_system_dir}/remote_ui'

        config_file = f'{T_SYSTEM_PATH}/remote_ui/config/{args["environment"]}.cfg'
        self.app.config.from_pyfile(config_file)

        Session(self.app)

        self.__set_app()

    def __set_app(self):
        """Method to setting flask API.
        """

        self.app.register_blueprint(access_api_bp)
        self.app.register_blueprint(face_encoding_api_bp)
        self.app.register_blueprint(identity_api_bp)
        self.app.register_blueprint(job_api_bp)
        self.app.register_blueprint(live_stream_api_bp)
        self.app.register_blueprint(move_api_bp)
        self.app.register_blueprint(network_api_bp)
        self.app.register_blueprint(position_api_bp)
        self.app.register_blueprint(r_sync_api_bp)
        self.app.register_blueprint(record_api_bp)
        self.app.register_blueprint(scenario_api_bp)
        self.app.register_blueprint(stream_api_bp)
        self.app.register_blueprint(system_info_api_bp)
        self.app.register_blueprint(update_api_bp)

        @self.app.route('/')
        def main():
            """Method to routing main.html .
            """

            return render_template('main.html')

    def run(self, host=None, port=None, debug=None):
        """Method to running flask with given parameters.

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


def allowed_file(filename, allowed_extensions):
    """The low-level method to check the given name compatibility that is for saving.

    Args:
        filename (string):          Name of file that will saved.
        allowed_extensions (set):   Allowed extensions.
    """

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


if __name__ == "__main__":

    app = RemoteUI(args={"host": "localhost", "port": "5000", "debug": True, "environment": "development"})
    app.run(host="0.0.0.0", port="5000",  debug=True)  # 0.0.0.0 means "all IPv4 addresses on the local machine"
    # app.debug = True
