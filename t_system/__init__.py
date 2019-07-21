#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of T_System that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import argparse  # Parser for command-line options, arguments and sub-commands
import sys  # System-specific parameters and functions
import os  # Miscellaneous operating system interfaces
import inspect  # Inspect live objects

from os.path import expanduser  # Common pathname manipulations
from picamera import PiCamera

from t_system.vision import Vision

__version__ = '0.9.4'

camera = PiCamera()

T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def start(args):
    """Function that starts the tracking system with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    vision = Vision(args, camera, (args["resolution"][0], args["resolution"][0]), args["framerate"])

    try:
        if args["interface"] == "official_stand":
            from t_system.stand import Stand

            stand = Stand(args, vision)
            stand.run()

        elif args["interface"] == "augmented":
            from t_system.augmented import Augmenter

            augmenter = Augmenter(vision)
            augmenter.run(lambda: False)

        elif args["interface"] == "remote_ui":
            from t_system.remote_ui import RemoteUI

            template_folder = T_SYSTEM_PATH + "/remote_ui/www"
            static_folder = template_folder + "/static"

            remote_ui = RemoteUI(template_folder=template_folder, static_folder=static_folder, vision=vision)
            remote_ui.run(host=args["host"], port=args["port"], debug=args["debug"])

        else:
            if args["learn"]:
                vision.learn(lambda: False)
            elif args["security"]:
                vision.security(lambda: False)
            else:
                vision.detect_track(lambda: False)

    except KeyboardInterrupt:
        vision.release_camera()
        vision.release_servos()


def prepare(args):
    """The function that prepares the working environment for storing data during running.

    Args:
        args:       Command-line arguments.
    """
    # AI SELECT PROCESSES WILL BE HERE.
    home = expanduser("~")
    dot_t_system_dir = home + "/.t_system"
    if not os.path.exists(dot_t_system_dir):
        os.mkdir(dot_t_system_dir)

    if not args["AI"]:
        if args["learn"]:
            raise Exception('All AI learning tools deprecated. Don\'t use the learn mode without AI.')


def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()

    w_mode_gr = ap.add_argument_group('user-interfaces')
    w_mode_gr.add_argument("interface", help="Set the user interfaces. To use: either `official_stand`, `augmented`, `remote_ui` or None."
                                             "`official_stand`: for using the interface of official T_System stand."
                                             "`augmented`: Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'."
                                             "remote_ui: remote control with created graphic interface that is power by flask available on desktop or mobile."
                                             "None: Use to just by `running modes` parameters."
                                             "The default value is None.", action="store", type=str, default="None")

    official_stand_gr = ap.add_argument_group('official_stand')
    official_stand_gr.add_argument("--stand-gpios", help="GPIO pin numbers of official stand's the button and the led. 5(as button), 27(as red led) and 22(as green led) GPIO pins are default.", nargs=3, default=[5, 25, 22], type=int, metavar=('BUTTON', 'RED-LED', 'GREEN-LED'))

    remote_ui_gr = ap.add_argument_group('remote_ui')
    remote_ui_gr.add_argument("--host", help="Specify host address.", action="store", type=str, default="localhost")
    remote_ui_gr.add_argument("--port", help="Specify the port.", action="store", type=str, default="4000")
    remote_ui_gr.add_argument("--debug", help="Activate debug mode.", action="store_true")

    r_mode_gr = ap.add_argument_group('running modes')
    r_mode_gr.add_argument("-l", "--learn", help="Teach Mode. Teach the object tracking parameters with the trial and error method.", action="store_true")
    r_mode_gr.add_argument("-s", "--security", help="Security Mode. Scan the around and optionally take photos of visitors.", action="store_true")
    # r_mode_gr.add_argument("-a", "--augmented", help="Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'.", action="store_true")

    tool_gr = ap.add_argument_group('running tools')
    tool_gr.add_argument("--AI", help="Specify the learning method of how to move to the target position from the current. When the nothing chosen, learn mode and decision mechanisms will be deprecated. to use: either `official_ai`", action="store", type=str)
    tool_gr.add_argument("--detection-model", help="Object detection model to use: either `haarcascade`, `hog` or `cnn`. `hog` and `cnn` can only use for detecting human faces. `haarcascade` is default.", action="store", type=str, default="haarcascade")
    tool_gr.add_argument("--cascade-file", help="Specify the trained detection algorithm file for the object detection ability. Sample: 'frontalface_default' for frontalface_default.xml file under the 'haarcascade' folder.", action="store", type=str, default="frontalface_default")
    tool_gr.add_argument("-j", "--no-recognize", help="Do not recognize the things.(faces, objects etc.)", action="store_true")
    tool_gr.add_argument("--encoding-file", help="Specify the trained recognition encoding pickle file for recognize object. Sample: 'encodings' for encodings.pickle file under the 'recognition_encodings' folder.", action="store", type=str, default="encodings")
    tool_gr.add_argument("--use-tracking-api", help="Use the openCV's tracking API for realize the next object is same as previous one.", action="store_true")
    tool_gr.add_argument("--tracker-type", help="OpenCV's tracking type to use: either `BOOSTING`, `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE` or `CSRT`. `CSRT` is default.", action="store", type=str, default="CSRT")
    tool_gr.add_argument("--resolution", help="Specify the camera's resolution of vision ability.", nargs=2, default=[320, 240], type=int, metavar=('WIDTH', 'HEIGHT'))
    tool_gr.add_argument("--framerate", help="Specify the camera's framerate. of vision ability", action="store", default=32, type=int)

    motion_gr = ap.add_argument_group('motion mechanism')
    motion_gr.add_argument("--locking-system-gpios", help="GPIO pin numbers of the 2 axis target locking system's servo motors. 17(as pan) and 25(as tilt) GPIO pins are default.", nargs=2, default=[17, 27], type=int, metavar=('PAN', 'TILT'))
    motion_gr.add_argument("--robotic-arm", help="One of the robotic arm names those are defined in arm_config.json file. The arm is for relocating the 2 axis target locking system hybrid-synchronously.", type=str, metavar=('ARM',))

    other_gr = ap.add_argument_group('others')
    other_gr.add_argument("-S", "--show-stream", help="Display the camera stream. Enable the stream window.(Require gui environment.)", action="store_true")
    other_gr.add_argument("-r", "--record", help="Record the video stream. Files are named by the date.", action="store_true")
    other_gr.add_argument("--version", help="Display the version number of T_System.", action="store_true")

    args = vars(ap.parse_args())

    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("t_system").version)
        sys.exit(1)
    prepare(args)
    start(args)


if __name__ == '__main__':
    initiate()
