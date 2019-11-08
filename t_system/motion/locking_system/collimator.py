#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: collimator
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to collimator of T_System's Target Locking System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import threading
from math import pi

from multipledispatch import dispatch

from t_system.motion.motor import ServoMotor, ExtServoMotor
from t_system.motion import degree_to_radian
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class Collimator:
    """Class to define a moving axis/joint the target locking system.

        This class provides necessary initiations and a function named :func:`t_system.motion.Mover.move`
        for the provide move of servo motor during locking to the target.

    """

    def __init__(self, out_number, frame_width, init_angle=pi / 2, is_reverse=True, use_ext_driver=None):
        """Initialization method of :class:`t_system.motion.LockingSystem` class.

        Args:
            out_number (tuple):     GPIO pin and servo driver channel to use for servo motor.
            frame_width:       	    Width of the camera's frame.
            init_angle:       	    Initialization angle value for servo motor as radian unit.
            use_ext_driver (bool):  The flag of external PWM driver activation.
        """

        self.frame_width = frame_width
        self.current_angle = init_angle
        self.previous_dis_to_des = 0.0

        self.is_reverse = is_reverse
        self.use_ext_driver = use_ext_driver

        if self.use_ext_driver:
            self.motor = ExtServoMotor(out_number[1])
            self.motor.start(round(self.current_angle, 4))
        else:
            self.motor = ServoMotor(out_number[0])
            self.motor.start(self.current_angle)

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

        delta_angle = self.__calc_delta_angle(obj_width, dis_to_des, k_fact)

        target_angle = self.__calc_target_angle(delta_angle)
        logger.debug(f'{target_angle}')

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
            angle = degree_to_radian(angle)
            self.motor.directly_goto_position(angle)
            self.current_angle = angle

    @dispatch(bool, bool)
    def move(self, stop, direction=True):
        """The top-level method to provide servo motors moving as incrementally and regular via threading.

        Args:
            stop:       	         Stop flag of the tread about terminating it outside of the function's loop.
            direction:       	     Direction of the moving.
        """

        self.motor_thread_stop = stop
        self.motor_thread_direction = direction

        if not self.is_reverse:
            self.motor_thread_direction = not self.motor_thread_direction

        if self.motor_thread.is_alive():
            # self.motor_thread.join()  # .join() attribute is for keep waited the main program until the thread ends.
            pass
        else:
            if not self.motor_thread_stop:
                self.motor_thread = threading.Thread(target=self.motor.change_position_incregular, args=(lambda: self.motor_thread_stop, lambda: self.motor_thread_direction))
                self.motor_thread.start()

    def __calc_target_angle(self, delta_angle):
        """Method to calculate what are going to be servo motors duty cycles.

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
        """Method to calculate the distance to the destination at that moment.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
        """
        obj_middle_px = (obj_first_px + obj_last_px) / 2
        frame_middle_px = self.frame_width / 2 - 1

        return float(obj_middle_px - frame_middle_px)

    @staticmethod
    def __calc_delta_angle(obj_width, dis_to_des, k_fact):
        """Method to calculate theta angle(delta angle) via k factor for reaching the destination position. In radian type.

        Theta angle, in radian type, is equal to divide the distance to the destination to physically distance of the object.
        And there is a relationship as the object's area / k factor with physical distance and object's area.

        Args:
            obj_width (int):         The width of the found object from haarcascade for measurement inference.
            dis_to_des:       	     distance from 'frame middle point' to ' object middle point' (distance to destination.)
            k_fact (float):          The factor related to object width for measurement inference.
        """

        return dis_to_des / (obj_width / k_fact)

    def get_previous_dis_to_des(self):
        """Method to provide return previous_dis_to_des variable.
        """
        if self.previous_dis_to_des == 0.0:
            self.previous_dis_to_des = 0.00001  # For avoid the 'float division by zero' error

        return self.previous_dis_to_des

    def restart(self, angle=None):
        """Method to provide stop the GPIO.PWM services that are reserved for the collimator's servo motor.

        Args:
            angle:              	 Restarting angle value for servo motor as radian unit.
        """
        if self.use_ext_driver:
            self.motor.__init__(self.motor.channel)
        else:
            self.motor.__init__(self.motor.gpio_pin)

        if angle:
            self.motor.start(angle)
        else:
            self.motor.start(self.current_angle)

    def stop(self):
        """Method to provide stop the GPIO.PWM services that are reserved for the collimator's servo motor.
        """
        if self.motor_thread.is_alive():
            self.motor_thread_stop = True
            self.motor_thread.join()

        self.motor.stop()

    def gpio_cleanup(self):
        """Method to provide clean the GPIO pins that are reserved for the collimator's servo motor.
        """
        self.motor.gpio_cleanup()
