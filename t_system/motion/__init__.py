#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the blocks related to checking T_System's motion ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import RPi.GPIO as GPIO
import time  # Time access and conversions

from t_system.motion.motor import ServoMotor

if __name__ == '__main__':

    # from gpiozero import AngularServo
    #
    # s = AngularServo(17)
    # try:
    #     while True:
    #         angle = -90
    #         while angle <= 90:
    #             s.angle = angle
    #             print(str(angle))
    #             angle += 30
    #             time.sleep(0.1)
    #         angle = 90
    #         while angle >= -90:
    #             s.angle = angle
    #             print(str(angle))
    #             angle -= 30
    #             time.sleep(0.1)

    # FOLLOWING LINES FOR THE TESTING THE "motion" SUBMODULE!!
    servoPIN = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(7.5)  # Initialization
    try:
        while True:
            duty_cy = 2.5
            while duty_cy <= 12.5:
                duty_cy = round(duty_cy, 3)
                p.ChangeDutyCycle(duty_cy)
                print(str(duty_cy))

                duty_cy += 1
                time.sleep(0.5)
            while duty_cy >= 2.5:
                duty_cy = round(duty_cy, 3)
                p.ChangeDutyCycle(duty_cy)
                print(str(duty_cy))

                duty_cy -= 1
                time.sleep(0.5)

        # p.ChangeDutyCycle(9)
        # time.sleep(1)
        # p.ChangeDutyCycle(7)
        # time.sleep(1)

    except KeyboardInterrupt:
        pass
        p.stop()
        GPIO.cleanup()
