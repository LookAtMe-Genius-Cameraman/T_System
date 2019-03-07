#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: motion
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's motion ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import RPi.GPIO as GPIO
import time

from t_system.decision import Decider

decider = Decider()


class Motion():
    """Class to define a motion of tracking system..

        This class provides necessary initiations and a function named :func:`t_system.Motion.move`
        for the provide move of servo motor.

    """

    def __init__(self, servo_pin, init_duty_cy=7.5):

        """Initialization method of :class:`t_system.Motion` class.

        Args:
            servo_pin:       	    GPIO pin to use for servo motor.
        """

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)

        self.servo = GPIO.PWM(servo_pin, 50)  # GPIO 17 for PWM with 50Hz
        self.servo.start(init_duty_cy)
        self.current_duty_cy = init_duty_cy
        self.previous_dis_to_des = 0.000
    # self.resolution = resolution

    def move(self, obj_first_px, obj_last_px, frame_width):
        """The top-level method to provide servo motors moving.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            frame_width:       	     Width of the camera's frame.
        """

        obj_width = obj_last_px - obj_first_px

        dis_to_des = self.current_dis_to_des(obj_first_px, obj_last_px, frame_width)

        k_fact = decider.decision(obj_width)
        target_duty_cy = self.calc_duty_cycle(obj_width, dis_to_des, k_fact)
        
        self.servo.ChangeDutyCycle(target_duty_cy)

        self.current_duty_cy = target_duty_cy
        self.previous_dis_to_des = dis_to_des

        return obj_width  # this return is for the control of the result of the move.

    def calc_duty_cycle(self, obj_width, dis_to_des, k_fact):
        """The top-level method to calculate what are going to be servo motors duty cycles.

        Args:
            obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            dis_to_des:       	     distance from 'frame middle point' to ' object middle point' (distance to destination.)
            k_fact (float):          The factor related to object width for measurement inferencing.
            current_duty_cy:       	 current duty cycle from angle of servo motors.
        """
        teta_radian = dis_to_des / (obj_width / k_fact)
        duty_cycle = teta_radian * 180 / 3.1416 / 18
        return self.current_duty_cy - duty_cycle  # this mines (-) for the camera's mirror effect.

    def current_dis_to_des(self, obj_first_px, obj_last_px, frame_width):
        """The top-level method to calculate the distance to the destination at that moment.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            frame_width:       	     Width of the camera's frame.
        """
        obj_middle_px = (obj_first_px + obj_last_px) / 2
        frame_middle_px = frame_width / 2 - 1

        return float(obj_middle_px - frame_middle_px)

    def get_previous_dis_to_des(self):
        """The top-level method to provide return previous_dis_to_des variable.
        """
        if self.previous_dis_to_des == float(0):
            self.previous_dis_to_des = 0.00001  # For avoid the 'float division by zero' error

        return self.previous_dis_to_des


if __name__ == '__main__':
    servoPIN = 14
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(7.5)  # Initialization
    try:
        while True:
            p.ChangeDutyCycle(2.5)
            print(2.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            print(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            print(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(10)
            print(10)
            time.sleep(1)
            p.ChangeDutyCycle(12.5)
            print(12.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            print(2.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            print(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(7.5)
            print(7.5)
            time.sleep(0.5)
            p.ChangeDutyCycle(5)
            print(5)
            time.sleep(0.5)
            p.ChangeDutyCycle(2.5)
            print(2.5)
            time.sleep(0.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
