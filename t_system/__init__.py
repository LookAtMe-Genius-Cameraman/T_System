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
import inspect
import os
import sys  # System-specific parameters and functions
from picamera.array import PiRGBArray
from picamera import PiCamera

from t_system.vision import Vision

__version__ = '0.2'

camera = PiCamera()

T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/haarcascade_frontalface_default.xml"

vision = Vision(camera, ccade_xml_file, (320, 240), 32)


def start(args):
    vision.rtime_detect()
# if else structures will be here

def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--teach", help="Teach mode. Teach the object tracking parameters with the trial and error method.", action="store_true")
    ap.add_argument("-a", "--augmented", help="Increase verbosity of log output.", action="store_true")
    ap.add_argument("--version", help="Display the version number of T_System.", action="store_true")
    args = vars(ap.parse_args())
    if args["version"]:
        import pkg_resources
        print(pkg_resources.get_distribution("t_system").version)
        sys.exit(1)
    start(args)


if __name__ == '__main__':
    initiate()
