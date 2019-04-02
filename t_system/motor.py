#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: motion
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's motion ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
# from multidispatch import multimethod
import RPi.GPIO as GPIO
import time
import math


class Motor():
    """Class to define a motion of tracking system.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, servo_pin, decider, init_duty_cy=7.5, is_reverse=True):

        """Initialization method of :class:`t_system.motor.Motor` class.

        Args:
            servo_pin:       	    GPIO pin to use for servo motor.
            decider:                decider object of Decider class.
            init_duty_cy:       	Initialization angle value for servo motor as duty cycle.
        """

        self.servo_pin = servo_pin
        self.decider = decider
        self.is_reverse = is_reverse

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        GPIO.setwarnings(False)

        self.servo = GPIO.PWM(servo_pin, 50)  # GPIO 17 for PWM with 50Hz
        self.servo.start(init_duty_cy)
        self.current_duty_cy = init_duty_cy
        self.previous_dis_to_des = 0.0

    # @multimethod(int, int, float)
    def move(self, obj_first_px, obj_last_px, frame_width=0.0):
        """The top-level method to provide servo motors moving.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            frame_width:       	     Width of the camera's frame.
        """

        obj_width = obj_last_px - obj_first_px

        dis_to_des = self.current_dis_to_des(obj_first_px, obj_last_px, frame_width)
        # if dis_to_des <= 5:  # for increasing the moving performance.
        #     return obj_width

        k_fact = self.decider.decision(obj_width)
        target_duty_cy, physically_distance = self.calc_duty_cycle(obj_width, dis_to_des, k_fact)
        
        self.servo.ChangeDutyCycle(target_duty_cy)

        self.current_duty_cy = target_duty_cy
        self.previous_dis_to_des = dis_to_des

        return obj_width, physically_distance  # this return is for the control of the result of the move.

    # @move.dispatch(float, float)
    def angular_move(self, angle, max_angle):
        """The top-level method to provide servo motors moving.

        Args:
            angle:       	         Servo motor's angle. Between 0 - 180 Degree.
            max_angle:       	     Servo motor's upper edge of the angle range.
        """
        target_duty_cy = self.single_duty_cycle(angle, max_angle)

        self.servo.ChangeDutyCycle(target_duty_cy)
        self.current_duty_cy = target_duty_cy

    def single_duty_cycle(self, angle, max_angle):
        """The top-level method to calculate what are going to be servo motors duty cycles.

        Args:
            angle:       	         Servo motor's angle. Between 0 - 180 Degree.
            max_angle:       	     Servo motor's upper edge of the angle range.
        """
        return angle / (max_angle / 10) + 2.5

    def calc_duty_cycle(self, obj_width, dis_to_des, k_fact):
        """The top-level method to calculate what are going to be servo motors duty cycles.

        Args:
            obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            dis_to_des:       	     distance from 'frame middle point' to ' object middle point' (distance to destination.)
            k_fact (float):          The factor related to object width for measurement inferencing.
        """
        physically_distance = obj_width / k_fact
        teta_radian = dis_to_des / physically_distance
        duty_cycle = teta_radian * 180 / 3.1416 / 18

        if self.is_reverse:
            if self.current_duty_cy - duty_cycle < 0.0 or self.current_duty_cy - duty_cycle > 100.0:
                return self.current_duty_cy, physically_distance
            return self.current_duty_cy - duty_cycle, physically_distance  # this mines (-) for the camera's mirror effect.
        else:
            if self.current_duty_cy + duty_cycle < 0.0 or self.current_duty_cy + duty_cycle > 100.0:
                return self.current_duty_cy, physically_distance
            return self.current_duty_cy + duty_cycle, physically_distance

    @staticmethod
    def current_dis_to_des(obj_first_px, obj_last_px, frame_width):
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
        if self.previous_dis_to_des == 0.0:
            self.previous_dis_to_des = 0.00001  # For avoid the 'float division by zero' error

        return self.previous_dis_to_des

    def gpio_cleanup(self):
        GPIO.cleanup(self.servo_pin)


def calc_ellipsoidal_angle(angle, pan_max, tilt_max):
    """The top-level method to calculate what is going to be angle of second axis to ellipsoidal scanning of the around.

    Args:
        angle:       	         Servo motor's angle. Between 0 - 180 Degree.
        pan_max:       	         Maximum angle value of the pan axis.
        tilt_max:       	     Maximum angle value of the tilt axis.
    """
    return float(90 - (math.sqrt((1 - (angle * angle) / (pan_max * pan_max)) * (tilt_max * tilt_max))))


if __name__ == '__main__':

    # FOLLOWING LINES FOR THE TESTING THE "motion" SUBMODULE!!
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
