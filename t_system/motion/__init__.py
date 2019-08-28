#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the blocks related to checking T_System's motion ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
from math import sqrt, pi

import RPi.GPIO as GPIO
import time  # Time access and conversions


def calc_ellipsoidal_angle(angle, pan_max, tilt_max):
    """The top-level method to calculate what is going to be angle of second axis to ellipsoidal scanning of the around.

    Args:
        angle:       	         Servo motor's angle. Between 0 - 180 Degree.
        pan_max:       	         Maximum angle value of the pan axis.
        tilt_max:       	     Maximum angle value of the tilt axis.
    """
    return float(90 - (sqrt((1 - (angle * angle) / (pan_max * pan_max)) * (tilt_max * tilt_max))))


def degree_to_radian(angle):
    """The top-level method to provide converting degree type angle to radian type angle.

    Args:
        angle:       	         Servo motor's angle. Between 0 - 180 Degree.
    """

    return angle * pi / 180


if __name__ == '__main__':

    # FOLLOWING LINES FOR THE TESTING THE "motion" SUBMODULE!!
    servo_pin = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)

    p = GPIO.PWM(servo_pin, 50)  # GPIO 17 for PWM with 50Hz
    p.start(11)  # Initialization
    time.sleep(1)

    try:
        print("loop starting")
        while True:
            duty_cy = 2.5
            while duty_cy <= 12.5:
                duty_cy = round(duty_cy, 3)
                p.ChangeDutyCycle(duty_cy)
                print(str(duty_cy))

                duty_cy += 1
                time.sleep(0.5)

            while True:
                p.ChangeDutyCycle(0)
                time.sleep(10)
                break

            while duty_cy >= 2.5:
                duty_cy = round(duty_cy, 3)
                p.ChangeDutyCycle(duty_cy)
                print(str(duty_cy))

                duty_cy -= 1
                time.sleep(0.5)

    except KeyboardInterrupt:
        pass
        p.stop()
        GPIO.cleanup()
