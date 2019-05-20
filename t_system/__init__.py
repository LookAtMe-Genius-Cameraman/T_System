#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of T_System that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

# import the necessary packages
import argparse
import sys  # System-specific parameters and functions

from picamera import PiCamera

from t_system.vision import Vision


__version__ = '0.9.1'


camera = PiCamera()


def start(args):
    """Function that starts the tracking system with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    vision = Vision(args, camera, (800, 600), 32)

    if args["interface"] == "official_stand":
        from t_system.stand import Stand

        stand = Stand(vision)
        stand.run()

    elif args["interface"] == "augmented":
        from t_system.augmented import Augmenter

        augmenter = Augmenter(vision)
        augmenter.run(lambda: False)

    else:
        if args["learn"]:
            vision.learn(lambda: False)
        elif args["security"]:
            vision.security(lambda: False)
        else:
            vision.detect_track(lambda: False)


def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()

    w_mode_gr = ap.add_argument_group('user-interfaces')
    w_mode_gr.add_argument("interface", help="Set the user interfaces. To use: either `official_stand`, `augmented` or None."
                                             "`official_stand`: for using the interface of official T_System stand."
                                             "`augmented`: Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'."
                                             "None: Use to just by `running modes` parameters."
                                             "The default value is None.", action="store", type=str, default="None")

    r_mode_gr = ap.add_argument_group('running modes')
    r_mode_gr.add_argument("-l", "--learn", help="Teach Mode. Teach the object tracking parameters with the trial and error method.", action="store_true")
    r_mode_gr.add_argument("-s", "--security", help="Security Mode. Scan the around and optionally take photos of visitors.", action="store_true")
    # r_mode_gr.add_argument("-a", "--augmented", help="Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'.", action="store_true")

    tool_gr = ap.add_argument_group('running tools')
    tool_gr.add_argument("--detection-model", help="Object detection model to use: either `haarcascade`, `hog` or `cnn`. `hog` and `cnn` can only use for detecting faces. `haarcascade` is default.", action="store", type=str, default="haarcascade")
    tool_gr.add_argument("--cascade-file", help="Specify the trained detection algorithm file for the object detection ability. Sample: 'frontalface_default' for frontalface_default.xml file under the 'haarcascade' folder.", action="store", type=str, default="frontalface_default")
    tool_gr.add_argument("-j", "--no-recognize", help="Do not recognize the things.(faces, objects etc.)", action="store_true")
    tool_gr.add_argument("--encoding-file", help="Specify the trained recognition encoding pickle file for recognize object. Sample: 'encodings' for encodings.pickle file under the 'recognition_encodings' folder.", action="store", type=str, default="encodings")
    tool_gr.add_argument("--use-tracking-api", help="Use the openCV's tracking API for realize the next object is same as previous one.", action="store_true")
    tool_gr.add_argument("--tracker-type", help="OpenCV's tracking type to use: either `BOOSTING`, `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE` or `CSRT`. `CSRT` is default.", action="store", type=str, default="CSRT")

    other_gr = ap.add_argument_group('others')
    other_gr.add_argument("-S", "--show-stream", help="Display the camera stream. Enable the stream window.(Require gui environment.)", action="store_true")
    other_gr.add_argument("-r", "--record", help="Record the video stream. Files are named by the date.", action="store_true")
    other_gr.add_argument("--servo-gpios", help="GPIO pin numbers of the 2 axis moving platform's servo motors. 17(as pan) and 25(as tilt) GPIO pins are default.", nargs=2, default=[17, 25], type=int, metavar=('PAN', 'TILT'))
    other_gr.add_argument("--version", help="Display the version number of T_System.", action="store_true")

    args = vars(ap.parse_args())

    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("t_system").version)
        sys.exit(1)

    start(args)


if __name__ == '__main__':
    initiate()
