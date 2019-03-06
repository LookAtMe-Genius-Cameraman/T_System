#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level module of T_System that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

# import the necessary packages
import inspect
import os
from picamera.array import PiRGBArray
from picamera import PiCamera

from t_system.vision import Vision

camera = PiCamera()

T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/haarcascade_frontalface_default.xml"

vision = Vision(camera, ccade_xml_file, (320, 240), 32)


def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """
    vision.rtime_detect()


if __name__ == '__main__':
    initiate()
