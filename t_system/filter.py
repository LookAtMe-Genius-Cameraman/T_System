#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: filter
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's data filter ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import numpy as np
from scipy.signal import butter, lfilter, freqz


class LowPassFilter:
    """Class to define an kind of filter.

        This class provides necessary initiations and a function named :func:`t_system.motion.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self):
        """Initialization method of :class:`t_system.motor.Motor` class.
        """

        pass

    @staticmethod
    def butter_low_pass(cutoff, fs, order=5):
        """Method to start of the motor initially.

        Args:
            init_angel (float):     Initialization angle value for servo motor in radian unit.
        """
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        c = butter(order, normal_cutoff, btype='low', analog=False)
        b = c[0]
        a = c[1]  # this lines would be like "b,a = ..." but there was a warning.
        return b, a

    def butter_low_pass_filter(self, data, cutoff, fs, order=5):
        """Method to start of the motor initially.

        Args:
            init_angel (float):     Initialization angle value for servo motor in radian unit.
        """
        b, a = self. butter_low_pass(cutoff, fs, order=order)
        y = lfilter(b, a, data)

        return y
