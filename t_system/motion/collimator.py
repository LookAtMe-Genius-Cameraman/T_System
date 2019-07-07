#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: collimator
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to collimator of T_System's Target Locking System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import threading
from math import sqrt, pi

from multipledispatch import dispatch

from t_system.motion import ServoMotor


def calc_ellipsoidal_angle(angle, pan_max, tilt_max):
    """The low-level method to calculate what is going to be angle of second axis to ellipsoidal scanning of the around.

    Args:
        angle:       	         Servo motor's angle. Between 0 - 180 Degree.
        pan_max:       	         Maximum angle value of the pan axis.
        tilt_max:       	     Maximum angle value of the tilt axis.
    """
    return float(90 - (sqrt((1 - (angle * angle) / (pan_max * pan_max)) * (tilt_max * tilt_max))))


class Collimator:
    """Class to define a moving axis/joint the target locking system.

        This class provides necessary initiations and a function named :func:`t_system.motion.Mover.move`
        for the provide move of servo motor during locking to the target.

    """

    def __init__(self, gpio_pin, frame_width, init_angle=pi/2, is_reverse=True):
        """Initialization method of :class:`t_system.motion.LockingSystem` class.

        Args:
            gpio_pin:       	    GPIO pin to use for servo motor.
            frame_width:       	     Width of the camera's frame.
            init_angle:       	    Initialization angle value for servo motor as radian unit.
        """

        self.frame_width = frame_width
        self.current_angle = init_angle
        self.previous_dis_to_des = 0.0

        self.is_reverse = is_reverse

        self.motor = ServoMotor(gpio_pin)
        self.motor.start(init_angle)

        self.motor_thread = None
        self.motor_thread_stop = None
        self.motor_thread_direction = None

        self.motor_thread = threading.Thread(target=self.motor.change_position_incregular, args=(lambda: self.motor_thread_stop, lambda: self.motor_thread_direction))

    @dispatch(int, int, int, float)
    def move(self, obj_first_px, obj_last_px, obj_width, k_fact):
        """The top-level method to provide servo motors moving.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            k_fact (float):          The factor related to object width for measurement inferencing.

        """

        dis_to_des = self.current_dis_to_des(obj_first_px, obj_last_px)

        delta_angle = self.calc_delta_angle(obj_width, dis_to_des, k_fact)

        target_angle = self.calc_target_angle(delta_angle)
        print(str(target_angle))
        if abs(target_angle - self.current_angle) < 0.01:  # 0.01 radian is equal to .5 degree.
            pass
        else:
            self.motor.directly_goto_position(target_angle)

        self.previous_dis_to_des = dis_to_des

    @dispatch(float, float)
    def move(self, angle, max_angle=180.0):
        """The top-level method to provide servo motors moving via given angles.

        Args:
            angle:       	         Servo motor's angle. Between 0 - 180 Degree.
            max_angle:       	     Servo motor's upper edge of the angle range.
        """

        if angle <= max_angle:
            angle = self.degree_to_radian(angle)
            self.motor.directly_goto_position(angle)
            self.current_angle = angle

    @dispatch(bool, bool)
    def move(self, stop, direction=True):
        """The top-level method to provide servo motors moving as incrementally and regular via threading.

        Args:
            stop:       	         Stop flag of the tread about terminating it outside of the function's loop.
            direction:       	     Direction of the moving.
        """
        # print(str(stop))
        self.motor_thread_stop = stop
        self.motor_thread_direction = direction

        if not self.is_reverse:
            self.motor_thread_direction = not self.motor_thread_direction

        if self.motor_thread.is_alive():
            # self.motor_thread.join()  # .join() attribute is for keep waited the main program until the thread ends.
            pass
        else:
            if not self.motor_thread_stop:
                # print("started")
                self.motor_thread = threading.Thread(target=self.motor.change_position_incregular, args=(lambda: self.motor_thread_stop, lambda: self.motor_thread_direction))
                self.motor_thread.start()

    @staticmethod
    def degree_to_radian(angle):
        """The top-level method to provide converting degree type angle to radian type angle.

        Args:
            angle:       	         Servo motor's angle. Between 0 - 180 Degree.
        """

        return angle * pi / 180

    def calc_target_angle(self, delta_angle):
        """The low-level method to calculate what are going to be servo motors duty cycles.

        Args:
            delta_angle (float):     Calculated theta angle for going to object position. In radian type.
        """

        if self.is_reverse:
            if self.current_angle - delta_angle < 0 or self.current_angle - delta_angle > pi:
                return self.current_angle
            return self.current_angle - delta_angle  # this mines (-) for the camera's mirror effect.
        else:
            if self.current_angle + delta_angle < 0 or self.current_angle + delta_angle > pi:
                return self.current_angle
            return self.current_angle + delta_angle

    def current_dis_to_des(self, obj_first_px, obj_last_px):
        """The low-level method to calculate the distance to the destination at that moment.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
        """
        obj_middle_px = (obj_first_px + obj_last_px) / 2
        frame_middle_px = self.frame_width / 2 - 1

        return float(obj_middle_px - frame_middle_px)

    @staticmethod
    def calc_delta_angle(obj_width, dis_to_des, k_fact):
        """The low-level method to calculate theta angle(delta angle) via k factor for reaching the destination position. In radian type.

        Theta angle, in radian type, is equal to divide the distance to the destination to physically distance of the object.
        And there is a relationship as the object's area / k factor with physical distance and object's area.

        Args:
            obj_width (int):         The width of the found object from haarcascade for measurement inference.
            dis_to_des:       	     distance from 'frame middle point' to ' object middle point' (distance to destination.)
            k_fact (float):          The factor related to object width for measurement inference.
        """

        return dis_to_des / (obj_width / k_fact)

    def get_previous_dis_to_des(self):
        """The low-level method to provide return previous_dis_to_des variable.
        """
        if self.previous_dis_to_des == 0.0:
            self.previous_dis_to_des = 0.00001  # For avoid the 'float division by zero' error

        return self.previous_dis_to_des
