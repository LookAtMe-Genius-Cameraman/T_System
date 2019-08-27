#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: motor
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's Servo Motors.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time  # Time access and conversions
import threading

from math import pi
from RPi import GPIO as GPIO

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class ServoMotor:
    """Class to define a servo motors of joints.

        This class provides necessary initiations and a function named :func:`t_system.motion.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, gpio_pin):
        """Initialization method of :class:`t_system.motor.Motor` class.

        Args:
            gpio_pin:       	    GPIO pin to use for servo motor.
        """

        self.gpio_pin = gpio_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setwarnings(False)

        self.servo = GPIO.PWM(gpio_pin, 50)  # GPIO pin for PWM with 50Hz

        self.max_duty_cy = 12.5
        self.min_duty_cy = 2.5
        self.current_duty_cy = None

        self.last_work_time = None
        self.sleep_listener_thread = threading.Thread(target=self.sleep_listener)

    def start(self, init_angel):
        """The high-level method to start of the motor initially.

        Args:
            init_angel (float):     Initialization angle value for servo motor in radian unit.
        """
        init_duty_cy = self.angle_to_duty_cy(init_angel)

        self.servo.start(init_duty_cy)
        self.current_duty_cy = init_duty_cy

        self.last_work_time = time.time()

        time.sleep(1)
        self.sleep()

    def low_pass_filter(self, init_angel):
        """The high-level method to start of the motor initially.

        Args:
            init_angel (float):     Initialization angle value for servo motor in radian unit.
        """
        init_duty_cy = self.angle_to_duty_cy(init_angel)

        self.servo.start(init_duty_cy)
        self.current_duty_cy = init_duty_cy

    @staticmethod
    def angle_to_duty_cy(theta_radian):
        """The low-level method to convert theta angle to the duty cycle.

        Args:
            theta_radian (float):     The position angle of servo motor. In radian type.
        """

        return (theta_radian * 180 / pi) / 18

    def directly_goto_position(self, target_angle):
        """The high-level method to changing position to the target angle.

        Args:
            target_angle (float):     The target position angle of servo motor. In radian type.
        """

        target_duty_cy = self.angle_to_duty_cy(target_angle)
        logger.debug(f' Target duty cycle of Motor in GPIO {self.gpio_pin} is {target_duty_cy}')

        if self.min_duty_cy <= target_duty_cy <= self.max_duty_cy:
            target_duty_cy = round(target_duty_cy, 5)

            self.change_duty_cycle(target_duty_cy)
            self.current_duty_cy = target_duty_cy
            logger.debug(f'Move of motor in GPIO {self.gpio_pin} completed')

    def softly_goto_position(self, target_angle):
        """The high-level method to changing position to the target angle step by step for more softly than direct_goto_position func.

        Args:
            target_angle (float):     The target position angle of servo motor. In radian type.
        """

        target_duty_cy = self.angle_to_duty_cy(target_angle)
        target_duty_cy = round(target_duty_cy, 5)

        # rotation will become from current_duty_cy to target duty_cy more softly. THESE LINES WILL BE EDITED WITH SOME FILTERS
        if target_duty_cy > self.current_duty_cy:
            delta_duty_cy = target_duty_cy - self.current_duty_cy

            while self.current_duty_cy < target_duty_cy:
                self.change_duty_cycle(self.current_duty_cy)
                self.current_duty_cy += delta_duty_cy / 50  # Divide the increasing to 50 parse.

        elif target_duty_cy < self.current_duty_cy:
            delta_duty_cy = self.current_duty_cy - target_duty_cy

            while self.current_duty_cy > target_duty_cy:
                self.change_duty_cycle(self.current_duty_cy)
                self.current_duty_cy -= delta_duty_cy / 50  # Each 0.055 decrease decreases the angle as 1 degree.
        else:
            self.change_duty_cycle(self.current_duty_cy)

        self.change_duty_cycle(target_duty_cy)

    def change_position_incregular(self, stop, direction):
        """The high-level method to changing position to the given direction as regularly and incremental when the stop flag is not triggered yet.

        Args:
            stop:                     The motion interrupt flag.
            direction:                The rotation way of servo motor. True is for clockwise, false is for can't clockwise.
        """
        increase = 0.11  # Each 0.055 increase of duty cycle value increases the angle as 1 degree. increase = 0.055 * 2
        timeout = 0

        while not stop():
            if timeout >= 5:  # 5 * 0.2 millisecond is equal to 1 second.
                break
            if direction():  # true direction is the left way
                if self.min_duty_cy <= self.current_duty_cy <= self.max_duty_cy:

                    self.current_duty_cy = self.current_duty_cy + increase
                    self.current_duty_cy = round(self.current_duty_cy, 4)
                    self.change_duty_cycle(self.current_duty_cy)

            else:
                if self.min_duty_cy <= self.current_duty_cy <= self.max_duty_cy:

                    self.current_duty_cy = self.current_duty_cy - increase
                    self.current_duty_cy = round(self.current_duty_cy, 4)
                    self.change_duty_cycle(self.current_duty_cy)
            timeout += 1

            time.sleep(0.2)

    def change_duty_cycle(self, duty_cycle):
        """The low-level method to handle changing duty-cycle of motor with listening sleep status for sending signal on unnecessary moments.

        Args:
            duty_cycle:               Cycle parameter of PWM signal.
        """

        self.servo.ChangeDutyCycle(duty_cycle)
        self.last_work_time = time.time()

        if not self.sleep_listener_thread.is_alive():
            self.sleep_listener_thread = threading.Thread(target=self.sleep_listener)
            self.sleep_listener_thread.start()

    def sleep_listener(self):
        """The low-level method to provide asynchronous listener to sending motor to sleep status with stop the signal sending to the PWM pin when work ended.
        """

        while True:
            time.sleep(1.5)
            if self.last_work_time < time.time():
                self.sleep()
                break

    def sleep(self):
        """The low-level method to provide stop the sending signal to motor's GPIO pin until coming new command.
        """

        self.servo.ChangeDutyCycle(0)  # If duty cycle has been set 0 (zero), no signal sending to GPIO pin.

    def stop(self):
        """The high-level method to provide stop the GPIO.PWM service that is reserved the servo motor.
        """
        self.servo.stop()

    def gpio_cleanup(self):
        """The high-level method to provide clean the GPIO pin that is reserved the servo motor.
        """
        GPIO.cleanup(self.gpio_pin)
