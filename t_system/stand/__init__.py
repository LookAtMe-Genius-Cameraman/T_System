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
from subprocess import call
import time  # Time access and conversions


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
        self.is_press_long = False
        self.press_count = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 10 to be an input pin and set initial value to be pulled low (off)

        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=self.set_press_state)  # Setup event on self.gpio_pin rising edge

    def set_press_state(self, channel):
        """The low-level method to provide callback event to catching button's press state.
        """
        start_time = time.time()
        # hold_time = start_time

        while GPIO.input(channel) == 0:  # Wait for the button up
            hold_time = time.time() - start_time  # How long was the button down?
            if hold_time >= 3:
                self.is_press_long = True
                break

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

    def __init__(self, vision):
        """Initialization method of :class:`t_system.stand.Stand` class.

        Args:
            vision:       	            Vision object from t_system.vision.Vision Class.
        """

        self.vision = vision

        self.standby_btn = Button(5)
        self.augmented_btn = Button(6)
        self.learn_btn = Button(13)
        self.track_btn = Button(19)

        self.red_led = Led(27)
        self.green_led = Led(22)

        self.stop_thread = False

    def run(self):
        """The top-level method to managing members of stand interface.
        """

        working_threads = []

        while True:
            print("running")
            if self.standby_btn.is_press_long:
                self.release_members()
                call("sudo poweroff", shell=True)
                break  # this line maybe not necessary!!

            elif self.standby_btn.is_pressed and self.standby_btn.press_count == 0:
                print("Stand By")
                self.reset_buttons(self.standby_btn, [self.augmented_btn, self.learn_btn, self.track_btn])
                self.terminate_threads(working_threads)

                self.start_thread(self.blink_led, (lambda: self.stop_thread, self.red_led), working_threads)

            elif self.augmented_btn.is_pressed and self.augmented_btn.press_count == 0:
                print("Augmented active")
                self.reset_buttons(self.augmented_btn, [self.standby_btn, self.learn_btn, self.track_btn])
                self.terminate_threads(working_threads)

                from t_system.augmented import Augmenter
                augmenter = Augmenter(self.vision)

                self.start_thread(augmenter.run, (lambda: self.stop_thread,), working_threads)
                self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led, [1, 30]), working_threads)

            elif self.learn_btn.is_pressed and self.learn_btn.press_count == 0:
                print("Learn active")
                self.reset_buttons(self.learn_btn, [self.standby_btn, self.augmented_btn, self.track_btn])
                self.terminate_threads(working_threads)

                self.start_thread(self.vision.learn, (lambda: self.stop_thread,), working_threads)
                self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led, [5, 5]), working_threads)

            elif self.track_btn.is_pressed and self.track_btn.press_count == 0:
                print("Track active")
                self.reset_buttons(self.track_btn, [self.standby_btn, self.augmented_btn, self.learn_btn])
                self.terminate_threads(working_threads)

                self.start_thread(self.vision.detect_track, (lambda: self.stop_thread,), working_threads)
                self.start_thread(self.blink_led, (lambda: self.stop_thread, self.green_led), working_threads)
            time.sleep(0.5)

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

    @staticmethod
    def reset_buttons(this_button, other_buttons):
        """The low-level method to releasing button states. Reset press count for other buttons and reset pressed state for currently pressed button.

        Args:
            this_button:       	        Button object that has been pressed.
            other_buttons (list):       The list of Button objects those are to be wanted to reset.
        """

        this_button.reset_press_state()

        for button in other_buttons:
            button.reset_press_count()

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

        self.vision.camera.release()
        self.vision.release_servos()

        self.standby_btn.gpio_cleanup()
        self.augmented_btn.gpio_cleanup()
        self.learn_btn.gpio_cleanup()
        self.track_btn.gpio_cleanup()

        self.red_led.gpio_cleanup()
        self.green_led.gpio_cleanup()
