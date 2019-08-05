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
from elevate import elevate  # partial root authentication interface

from t_system.vision import Vision
from t_system.accession import AccessPoint
from t_system.administration import Administrator

__version__ = '0.9-alpha1.79'

T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

home = expanduser("~")
dot_t_system_dir = home + "/.t_system"

seer = None
augmenter = None
stand_ui = None
administrator = None


def start(args):
    """Function that starts the tracking system with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """
    global seer
    global augmenter
    global stand_ui

    seer = Vision(args)

    try:
        if args["interface"] == "official_stand":
            from t_system.stand import Stand
            from t_system.remote_ui import RemoteUI

            template_folder = T_SYSTEM_PATH + "/remote_ui/www"
            static_folder = template_folder + "/static"

            remote_ui = RemoteUI(args=args, template_folder=template_folder, static_folder=static_folder, vision=seer)

            stand_ui = Stand(args, remote_ui)
            stand_ui.run()

        elif args["interface"] == "augmented":
            from t_system.augmented import Augmenter

            augmenter = Augmenter(seer)
            augmenter.run(lambda: False)

        elif args["interface"] == "remote_ui":
            from t_system.remote_ui import RemoteUI

            template_folder = T_SYSTEM_PATH + "/remote_ui/www"
            static_folder = template_folder + "/static"

            remote_ui = RemoteUI(args=args, template_folder=template_folder, static_folder=static_folder, vision=seer)
            remote_ui.run(host=args["host"], port=args["port"], debug=args["debug"])

        else:
            if args["learn"]:
                seer.learn(lambda: False)
            elif args["security"]:
                seer.security(lambda: False)
            else:
                seer.detect_track(lambda: False)

    except KeyboardInterrupt:
        seer.release_camera()
        seer.release_servos()
        seer.release_hearer()


def start_sub(args):
    """Function that starts the tracking system with the sub jobs according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    if args["sub_jobs"] == "remote-ui-authentication":
        administrator.change_keys(args["ssid"], args["password"])

    elif args["sub_jobs"] == "face-encoding":
        from t_system.face_encoding import FaceEncodeManager

        face_encode_manager = FaceEncodeManager(args["detection_method"])
        face_encode_manager.add_face(args["owner_name"], args["dataset"])

    if args["sub_jobs"] == "self-update":
        from t_system.updation import Updater, install

        updater = Updater(args)
        updater.update()

        install(args["editable"])


def prepare(args):
    """The function that prepares the working environment for storing data during running.

    Args:
        args:       Command-line arguments.
    """
    global administrator

    administrator = Administrator()

    if not os.path.exists(dot_t_system_dir):
        os.mkdir(dot_t_system_dir)

    if args["sub_jobs"]:
        start_sub(args)
        sys.exit(1)

    if args["access_point"]:
        with elevate(show_console=False, graphical=False):
            access_point = AccessPoint(args)
            access_point.start()

    if not args["AI"] or args["non_moving_target"]:
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
    tool_gr.add_argument("--detection-model", help="Object detection model to use: either `haarcascade`, `hog` or `cnn`. `hog` and `cnn` can only use for detecting human faces. `haarcascade` is default.", action="store", type=str, default="haarcascade")
    tool_gr.add_argument("--cascade-file", help="Specify the trained detection algorithm file for the object detection ability. Sample: 'frontalface_default' for frontalface_default.xml file under the 'haarcascade' folder.", action="store", type=str, default="frontalface_default")
    tool_gr.add_argument("-j", "--no-recognize", help="Do not recognize the things.(faces, objects etc.)", action="store_true")
    tool_gr.add_argument("--encoding-file", help="Specify the trained recognition encoding pickle file for recognize object. Sample: 'encodings' for encodings.pickle file under the 'recognition_encodings' folder.", action="store", type=str, default="encodings")
    tool_gr.add_argument("--use-tracking-api", help="Use the openCV's tracking API for realize the next object is same as previous one.", action="store_true")
    tool_gr.add_argument("--tracker-type", help="OpenCV's tracking type to use: either `BOOSTING`, `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE` or `CSRT`. `CSRT` is default.", action="store", type=str, default="CSRT")

    video_gr = ap.add_argument_group('video options')
    video_gr.add_argument("--resolution", help="Specify the camera's resolution of vision ability. 320x240 is default", nargs=2, default=[320, 240], type=int, metavar=('WIDTH', 'HEIGHT'))
    video_gr.add_argument("--framerate", help="Specify the camera's framerate. of vision ability. 32 fps is default.", action="store", default=32, type=int)
    video_gr.add_argument("--chunk", help="Smallest unit of audio. 1024*8=8192 bytes are default.", action="store", default=8192, type=int)
    video_gr.add_argument("--rate", help="Bit Rate of audio stream / Frame Rate. 44100 Hz sample rate is default.", action="store", default=44100, type=int)
    video_gr.add_argument("--channels", help="Number of microphone's channels. Default value is 1.", action="store", default=1, type=int)
    video_gr.add_argument("--audio_device_index", help="Index of the using audio device. 0 is default.", action="store", default=0, type=int)

    motion_gr = ap.add_argument_group('motion mechanism')
    motion_gr.add_argument("--robotic-arm", help="One of the robotic arm names those are defined in arm_config.json file. The arm is for relocating the 2 axis target locking system hybrid-synchronously.", type=str, metavar=('ARM',))

    lock_sys_gr = ap.add_argument_group('target locking system')
    lock_sys_gr.add_argument("--ls-gpios", help="GPIO pin numbers of the 2 axis target locking system's servo motors. 23(as pan) and 24(as tilt) GPIO pins are default.", nargs=2, default=[23, 24], type=int, metavar=('PAN', 'TILT'))
    lock_sys_usage_gr = lock_sys_gr.add_mutually_exclusive_group()
    lock_sys_usage_gr.add_argument("--AI", help="Specify the learning method of how to move to the target position from the current. When the nothing chosen, learn mode and decision mechanisms will be deprecated. to use: either `official_ai`", action="store", type=str, default=None)
    lock_sys_usage_gr.add_argument("--non-moving-target", help="Track the non-moving objects. Don't use AI or OpenCv's object detection methods. Just try to stay focused on the current focus point with changing axis angles by own position.", action="store_true")

    access_p_gr = ap.add_argument_group('access point options')
    access_p_gr.add_argument("-p", "--access-point", help="Become access point for serving remote UI inside the internal network.", action="store_true")
    access_p_gr.add_argument("--ap-wlan", help="network interface that will be used to create hotspot. 'wlp4s0' is default.", action="store", default="wlp4s0", type=str)
    access_p_gr.add_argument("--ap-inet", help="forwarding interface. Default is None.", action="store", default=None, type=str)
    access_p_gr.add_argument("--ap-ip", help="ip address of this machine in new network. 192.168.45.1 is default.", action="store", default="192.168.45.1", type=str)
    access_p_gr.add_argument("--ap-netmask", help="access point netmask address. 255.255.255.0 is default.", action="store", default="255.255.255.0", type=str)
    access_p_gr.add_argument("--ssid", help="Preferred access point name. 'T_System' is default.", action="store", default="T_System", type=str)
    access_p_gr.add_argument("--password", help="Password of the access point. 't_system' is default.", action="store", default="t_system", type=str)

    ext_network_gr = ap.add_argument_group('external network options')
    # ext_network_gr.add_argument("-p", "--access-point", help="Become access point for serving remote UI inside the internal network.", action="store_true")
    ext_network_gr.add_argument("--wlan", help="network interface that will be used to connect to external network. 'wlp4s0' is default.", action="store", default="wlp4s0", type=str)
    access_p_gr.add_argument("--inet", help="forwarding interface. Default is None.", action="store", default=None, type=str)
    access_p_gr.add_argument("--static-ip", help="static ip address in connected external network. 192.168.45.1 is default.", action="store", default="192.168.45.1", type=str)
    access_p_gr.add_argument("--netmask", help="netmask address. 255.255.255.0 is default.", action="store", default="255.255.255.0", type=str)

    other_gr = ap.add_argument_group('others')
    other_gr.add_argument("-S", "--show-stream", help="Display the camera stream. Enable the stream window.(Require gui environment.)", action="store_true")
    other_gr.add_argument("-m", "--found-object-mark", help="Specify the mark type of the found object.  To use: either `single_rect`, `rotating_arcs`, `partial_rect` or None. Default is `single_rect`", action="store", default="single_rect", type=str)
    other_gr.add_argument("-r", "--record", help="Record the video stream. Files are named by the date.", action="store_true")
    other_gr.add_argument("--version", help="Display the version number of T_System.", action="store_true")

    sub_p = ap.add_subparsers(dest="sub_jobs", help='officiate the sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_r_ui_auth = sub_p.add_parser('remote-ui-authentication', help='remote UI administrator authority settings of the secret entry point that is the new network connection panel.')
    ap_r_ui_auth.add_argument('--ssid', help='secret administrator ssid flag', type=str)
    ap_r_ui_auth.add_argument('--password', help='secret administrator password flag', type=str)

    ap_face_encode = sub_p.add_parser('face-encoding', help='generate encoded data from the dataset folder to recognize the man T_System is monitoring during operation.')
    ap_face_encode.add_argument("-i", "--dataset", help="path to input directory of faces + images.", required=True)
    ap_face_encode.add_argument("-n", "--owner-name", default=None, help="name of the images owner. If there is single man who has the images, give the name of that man with dataset", type=str)
    ap_face_encode.add_argument("-d", "--detection-method", help="face detection model to use: either `hog` or `cnn` default is `hog`", type=str, default="hog")

    ap_self_update = sub_p.add_parser('self-update', help='update source code of t_system itself via `git pull` command from the remote git repo.')
    ap_self_update.add_argument("-v", "--verbose", help="Print various debugging information to debug problems", action="store_true")
    ap_self_update.add_argument("-e", "--editable", help="Update the T_System in editable mode (i.e. setuptools'develop mode')", action="store_true")

    args = vars(ap.parse_args())

    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("t_system").version)
        sys.exit(1)
    prepare(args)
    start(args)


if __name__ == '__main__':
    initiate()
