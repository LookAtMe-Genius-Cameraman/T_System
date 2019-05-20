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
import time  # Time access and conversions
from math import sqrt, pi


class Motor:
    """Class to define a motion of tracking system.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, gpio_pin, decider, init_duty_cy=7.5, is_reverse=True):
        """Initialization method of :class:`t_system.motor.Motor` class.

        Args:
            gpio_pin:       	    GPIO pin to use for servo motor.
            decider:                decider object of Decider class.
            init_duty_cy:       	Initialization angle value for servo motor as duty cycle.
        """

        self.gpio_pin = gpio_pin
        self.decider = decider
        self.is_reverse = is_reverse

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setwarnings(False)

        self.servo = GPIO.PWM(gpio_pin, 50)  # GPIO 17 for PWM with 50Hz
        self.servo.start(init_duty_cy)

        self.current_duty_cy = init_duty_cy
        self.previous_dis_to_des = 0.0

    # @multimethod(int, int, float)
    def move(self, obj_first_px, obj_last_px, obj_area, frame_width=0.0):
        """The top-level method to provide servo motors moving.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            obj_area (int):          Area of the found object from haarcascade for measurement inferencing.
            frame_width:       	     Width of the camera's frame.
        """

        dis_to_des = self.current_dis_to_des(obj_first_px, obj_last_px, frame_width)

        k_fact = self.decider.decision(obj_area)
        theta_radian = self.calc_theta_angle(obj_area, dis_to_des, k_fact)
        target_duty_cy = self.calc_target_duty_cycle(theta_radian)

        # rotation will become from current_duty_cy to target duty_cy more softly.
        if target_duty_cy > self.current_duty_cy:
            while self.current_duty_cy < target_duty_cy:
                self.servo.ChangeDutyCycle(self.current_duty_cy)
                self.current_duty_cy += 0.055 * 2  # Each 0.055 increase increases the angle as 1 degree.

        elif target_duty_cy < self.current_duty_cy:
            while self.current_duty_cy > target_duty_cy:
                self.servo.ChangeDutyCycle(self.current_duty_cy)
                self.current_duty_cy -= 0.055 * 2  # Each 0.055 decrease decreases the angle as 1 degree.
        else:
            self.servo.ChangeDutyCycle(self.current_duty_cy)

        self.previous_dis_to_des = dis_to_des

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

    @staticmethod
    def single_duty_cycle(angle, max_angle):
        """The top-level method to calculate what are going to be servo motors duty cycles.

        Args:
            angle:       	         Servo motor's angle. Between 0 - 180 Degree.
            max_angle:       	     Servo motor's upper edge of the angle range.
        """
        return angle / (max_angle / 10) + 2.5

    def calc_target_duty_cycle(self, theta_radian):
        """The low-level method to calculate what are going to be servo motors duty cycles.

        Args:
            theta_radian (float):     Calculated theta angle for going to object position. In radian type.
        """

        duty_cycle = self.angle_to_duty_cy(theta_radian)

        if self.is_reverse:
            if self.current_duty_cy - duty_cycle < 0.0 or self.current_duty_cy - duty_cycle > 12.5:
                return self.current_duty_cy
            return self.current_duty_cy - duty_cycle  # this mines (-) for the camera's mirror effect.
        else:
            if self.current_duty_cy + duty_cycle < 0.0 or self.current_duty_cy + duty_cycle > 12.5:
                return self.current_duty_cy
            return self.current_duty_cy + duty_cycle

    @staticmethod
    def calc_theta_angle(obj_area, dis_to_des, k_fact):
        """The low-level method to calculate theta angle via k factor for reaching the destination position. In radian type.

        Theta angle, in radian type, is equal to divide the distance to the destination to physically distance of the object.
        And there is a relationship as the object's area / k factor with physical distance and object's area.

        Args:
            obj_area (int):          Area of the found object from haarcascade for measurement inferencing.
            dis_to_des:       	     distance from 'frame middle point' to ' object middle point' (distance to destination.)
            k_fact (float):          The factor related to object width for measurement inferencing.
        """

        return dis_to_des / (obj_area / k_fact)

    @staticmethod
    def angle_to_duty_cy(theta_radian):
        """The low-level method to convert theta angle to the duty cycle.

        Args:
            theta_radian (float):     Calculated theta angle for going to object position. In radian type.
        """

        return (theta_radian * 180 / pi) / 18

    @staticmethod
    def current_dis_to_des(obj_first_px, obj_last_px, frame_width):
        """The low-level method to calculate the distance to the destination at that moment.

        Args:
            obj_first_px:       	 initial pixel value of found object from haarcascade.
            obj_last_px:       	     last pixel value of found object from haarcascade.
            frame_width:       	     Width of the camera's frame.
        """
        obj_middle_px = (obj_first_px + obj_last_px) / 2
        frame_middle_px = frame_width / 2 - 1

        return float(obj_middle_px - frame_middle_px)

    def get_previous_dis_to_des(self):
        """The low-level method to provide return previous_dis_to_des variable.
        """
        if self.previous_dis_to_des == 0.0:
            self.previous_dis_to_des = 0.00001  # For avoid the 'float division by zero' error

        return self.previous_dis_to_des

    def get_physically_distance(self, obj_area):
        """The low-level method to provide return the tracking object's physically distance value.
        """
        k_fact = self.decider.decision(obj_area)

        return obj_area / k_fact  # physically distance is equal to obj_area / k_fact.

    def stop(self):
        """The low-level method to provide stop the GPIO.PWM service that is reserved the servo motor.
        """
        self.servo.stop()

    def gpio_cleanup(self):
        """The low-level method to provide clean the GPIO pin that is reserved the servo motor.
        """
        GPIO.cleanup(self.gpio_pin)


def calc_ellipsoidal_angle(angle, pan_max, tilt_max):
    """The low-level method to calculate what is going to be angle of second axis to ellipsoidal scanning of the around.

    Args:
        angle:       	         Servo motor's angle. Between 0 - 180 Degree.
        pan_max:       	         Maximum angle value of the pan axis.
        tilt_max:       	     Maximum angle value of the tilt axis.
    """
    return float(90 - (sqrt((1 - (angle * angle) / (pan_max * pan_max)) * (tilt_max * tilt_max))))


if __name__ == '__main__':

    # FOLLOWING LINES FOR THE TESTING THE "motion" SUBMODULE!!
    servoPIN = 17
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
