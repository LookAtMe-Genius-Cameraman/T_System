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


__version__ = '0.9'


camera = PiCamera()


def start(args):
    """Function that starts the tracking system with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    vision = Vision(args, camera, (800, 600), 32)

    if args["learn"]:
        vision.learn(lambda: False)
    elif args["security"]:
        vision.security(lambda: False)
    elif args["augmented"]:
        from t_system.augmentation import Augmenter

        augmenter = Augmenter(vision)
        augmenter.run()
    else:
        vision.detect_track(lambda: False)


def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-S", "--show-stream", help="Display the camera stream. Enable the stream window.", action="store_true")
    ap.add_argument("-l", "--learn", help="Teach Mode. Teach the object tracking parameters with the trial and error method.", action="store_true")
    ap.add_argument("-s", "--security", help="Security Mode. Scan the around and optionally take photos of visitors.", action="store_true")
    ap.add_argument("-a", "--augmented", help="Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'.", action="store_true")
    ap.add_argument("--version", help="Display the version number of T_System.", action="store_true")
    ap.add_argument("--cascadefile", help="Specify the trained detection algorithm file for the object detection ability. Sample(And Default): 'haarcascade_frontalface_default' for haarcascade_frontalface_default.xml file inside the 'haarcascade' folder. ", action="store", type=str)

    args = vars(ap.parse_args())

    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("t_system").version)
        sys.exit(1)

    start(args)


if __name__ == '__main__':
    initiate()
