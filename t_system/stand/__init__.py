#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's official stand interface.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import RPi.GPIO as GPIO
import threading
import time  # Time access and conversions

from subprocess import call
from elevate import elevate  # partial root authentication interface

from t_system.accession import NetworkConnector, AccessPoint

__version__ = '0.3'


class Button:
    """Class to define input buttons of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Button.set_press_state`
        for holding press event info.

    """

    def __init__(self, gpio_pin):
        """Initialization method of :class:`t_system.stand.Button` class.

        Args:
            gpio_pin (int):       	    GPIO pin to use for button.
        """

        self.gpio_pin = gpio_pin

        self.is_pressed = False
        self.pressed_hold_time = 0
        self.press_count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)

        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=self.set_press_state)  # Setup event on self.gpio_pin rising edge

    def set_press_state(self, channel):
        """The low-level method to provide callback event to catching button's press state.
        """
        start_time = time.time()

        while GPIO.input(channel) == 0:  # Wait for the button up
            self.pressed_hold_time = time.time() - start_time  # How long was the button down?
            time.sleep(0.1)
            pass

        # if hold_time >= .1:  # ignore noise
        #     self.is_pressed = True
        #     self.increase_press_count()

        self.is_pressed = True
        self.increase_press_count()

    def reset_press_state(self):
        """The top-level method to provide resetting of button's press state.
        """
        self.is_pressed = False

    def increase_press_count(self):
        """The low-level method to provide increasing of button's press count value.
        """
        self.press_count += 1

    def reset_press_count(self):
        """The top-level method to provide resetting of button's press count.
        """
        self.press_count = 0

    def reset_pressed_hold_time(self):
        """The top-level method to provide resetting of button's pressed hold time.
        """
        self.pressed_hold_time = 0

    def gpio_cleanup(self):
        """The low-level method to provide clean the GPIO pin that is reserved the button.
        """
        GPIO.cleanup(self.gpio_pin)


class Led:
    """Class to define input buttons of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Button.set_press_state`
        for holding press event info.

    """

    def __init__(self, gpio_pin):
        """Initialization method of :class:`t_system.stand.Button` class.

        Args:
            gpio_pin (int):       	    GPIO pin to use for button.
        """

        self.gpio_pin = gpio_pin

        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def on(self):
        """The top-level method to provide turning on the led.
        """
        GPIO.output(self.gpio_pin, GPIO.HIGH)

    def off(self):
        """The top-level method to provide turning off the led.
        """
        GPIO.output(self.gpio_pin, GPIO.LOW)

    def gpio_cleanup(self):
        """The low-level method to provide clean the GPIO pin that is reserved the led.
        """
        GPIO.cleanup(self.gpio_pin)


class Stand:
    """Class to define tracking system's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, args, remote_ui):
        """Initialization method of :class:`t_system.stand.Stand` class.

        Args:
            args:                       Command-line arguments.
        """

        self.network_connector = NetworkConnector(args)
        self.access_point = AccessPoint(args)

        self.remote_ui = remote_ui
        self.static_ip = args["static_ip"]

        self.multi_func_btn = Button(args["stand_gpios"][0])

        self.red_led = Led(args["stand_gpios"][1])
        self.green_led = Led(args["stand_gpios"][2])

        self.stop_thread = False

    def run(self):
        """The top-level method to managing members of stand interface.
        """
        if self.network_connector.connect():
            pass
        else:
            self.access_point.start()

        self.remote_ui.run(host=self.static_ip)

        # working_threads = []
        #
        # while True:
        #     print("running")
        #     if self.multi_func_btn.pressed_hold_time >= 3:
        #         self.release_members()
        #         call("sudo poweroff", shell=True)
        #         break  # this line maybe not necessary!!
        #
        #     elif self.multi_func_btn.pressed_hold_time >= 1.5:
        #         print("Stand By")
        #         self.multi_func_btn.reset_pressed_hold_time()
        #         self.reset_button()
        #         self.terminate_threads(working_threads)
        #
        #         self.start_thread(self.blink_led, (lambda: self.stop_thread, self.red_led), working_threads)
        #
        #     elif self.multi_func_btn.is_pressed and self.multi_func_btn.press_count == 3:
        #         print("Augmented active")
        #         self.reset_button()
        #         self.terminate_threads(working_threads)
        #
        #         from t_system.augmented import Augmenter
        #         augmenter = Augmenter(self.vision)
        #
        #         self.start_thread(augmenter.run, (lambda: self.stop_thread,), working_threads)
        #         self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led, [1, 30]), working_threads)
        #
        #     elif self.multi_func_btn.is_pressed and self.multi_func_btn.press_count == 2:
        #         print("Learn active")
        #         self.reset_button()
        #         self.terminate_threads(working_threads)
        #
        #         self.start_thread(self.vision.learn, (lambda: self.stop_thread,), working_threads)
        #         self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led, [5, 5]), working_threads)
        #
        #     elif self.multi_func_btn.is_pressed and self.multi_func_btn.press_count == 1:
        #         print("Track active")
        #         self.reset_button()
        #         self.terminate_threads(working_threads)
        #
        #         self.start_thread(self.vision.detect_track, (lambda: self.stop_thread,), working_threads)
        #         self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led), working_threads)
        #     time.sleep(0.5)

    def blink_led(self, stop_thread, led, delay_time=None):
        """The low-level method to blinking the LEDs with different on/off combinations.

        Args:
            stop_thread:   	            Stop flag of the tread about terminating it outside of the function's loop.
            led:       	                The Led object that is going be blinking.
            delay_time (list):          The delay time list in seconds, between blinks. Index 0 is time after led on and index 1 is after led off.
        """
        self.reset_leds()

        if delay_time:
            while True:
                if stop_thread():
                    break
                led.on()
                time.sleep(delay_time[0])

                led.off()
                time.sleep(delay_time[1])
        else:
            led.on()

    def reset_leds(self):
        """The low-level method to turning off the all led lights.
        """
        self.red_led.off()
        self.green_led.off()

    def reset_button(self):
        """The low-level method to releasing button states. Reset press count for other buttons and reset pressed state for currently pressed button.
        """

        self.multi_func_btn.reset_press_state()
        self.multi_func_btn.reset_press_count()
        self.multi_func_btn.reset_pressed_hold_time()

    @staticmethod
    def start_thread(job, job_args, working_threads):
        """The low-level method to starting new thread.

        Args:
            job:                        The function that is going to applied with multiprocessing.
            job_args (tuple):           Arguments of the job.
            working_threads (list):     List of working threads.
        """

        thread = threading.Thread(target=job, args=job_args)
        working_threads.append(thread)
        thread.start()

    def terminate_threads(self, working_threads):
        """The low-level method to killing existing threads/running modes.

        Args:
            working_threads (list):     List of working threads.
        """

        self.stop_thread = True
        for worker in working_threads:  # For checking the existing thread.
            worker.join()
        working_threads.clear()
        self.stop_thread = False

    def release_members(self):
        """The low-level method to releasing camera, stop sending signals and clean up the gpio pins.
        """

        self.vision.release_camera()
        self.vision.release_servos()

        self.multi_func_btn.gpio_cleanup()

        self.red_led.gpio_cleanup()
        self.green_led.gpio_cleanup()
