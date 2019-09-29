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

from t_system.accession.__init__ import NetworkConnector, AccessPoint
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")

__version__ = '0.3.12'


class Button:
    """Class to define input buttons of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Button.__set_press_state`
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

        GPIO.add_event_detect(self.gpio_pin, GPIO.RISING, callback=self.__set_press_state)  # Setup event on self.gpio_pin rising edge

    def __set_press_state(self, channel):
        """Method to provide callback event to catching button's press state.
        """
        start_time = time.time()

        while GPIO.input(channel) == 0:  # Wait for the button up
            self.pressed_hold_time = time.time() - start_time  # How long was the button down?
            time.sleep(0.1)
            pass

        # if hold_time >= .1:  # ignore noise
        #     self.is_pressed = True
        #     self.__increase_press_count()

        self.is_pressed = True
        self.__increase_press_count()

    def reset_press_state(self):
        """The top-level method to provide resetting of button's press state.
        """
        self.is_pressed = False

    def __increase_press_count(self):
        """Method to provide increasing of button's press count value.
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
        """The top-level method to provide clean the GPIO pin that is reserved the button.
        """
        GPIO.cleanup(self.gpio_pin)


class Led:
    """Class to define sign LEDs of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Led.on`
        for activating the LED and a function named :func:`t_system.stand.Led.off` for deactivating the LED.

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
        """The top-level method to provide clean the GPIO pin that is reserved the led.
        """
        GPIO.cleanup(self.gpio_pin)


class Fan:
    """Class to define cooler fans of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Fan.change_speed`
        for changing revolute speed by incoming percent value.

    """

    def __init__(self, gpio_pin):
        """Initialization method of :class:`t_system.stand.Fan` class.

        Args:
            gpio_pin (int):       	    GPIO pin to use for Fan.
        """

        self.gpio_pin = gpio_pin

        self.gpio_pin = gpio_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.setwarnings(False)

        self.servo = GPIO.PWM(gpio_pin, 50)  # GPIO pin for PWM with 50Hz

        self.max_duty_cy = 12.5
        self.min_duty_cy = 2.5
        self.current_duty_cy = None

    def start(self, init_percent):
        """Method to start of the fan initially.

        Args:
            init_percent (float):     Initialization percentage speed value for the fan.
        """
        init_duty_cy = self.__percent_to_duty_cy(init_percent)

        self.servo.start(init_duty_cy)
        self.current_duty_cy = init_duty_cy

    def change_speed(self, speed_percent):
        """Method to change of fan speed.

        Args:
            speed_percent (float):     Percentage speed value for the fan to set to it.
        """

        if speed_percent == 0:
            self.__sleep()

        self.__change_duty_cycle(self.__percent_to_duty_cy(speed_percent))

    def __change_duty_cycle(self, duty_cycle):
        """Method to handle changing duty-cycle of fan by given duty cycle value.

        Args:
            duty_cycle:               Cycle parameter of PWM signal.
        """

        self.servo.ChangeDutyCycle(duty_cycle)

    def __percent_to_duty_cy(self, percent):
        """Method to convert percentage to the duty cycle.

        Args:
            percent (float):     The speed percentage of the cooler fan.
        """

        return (percent / 100) * (self.max_duty_cy - self.min_duty_cy) + self.min_duty_cy

    def __sleep(self):
        """Method to provide stop the sending signal to fan's GPIO pin until coming new command.
        """

        self.servo.ChangeDutyCycle(0)  # If duty cycle has been set 0 (zero), no signal sending to GPIO pin.

    def stop(self):
        """Method to provide stop the GPIO.PWM service that is reserved the fan.
        """

        self.servo.stop()

    def gpio_cleanup(self):
        """Method to provide clean the GPIO pin that is reserved the fan.
        """

        GPIO.cleanup(self.gpio_pin)


class Cooler:
    """Class to define cooler of T_System's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.stand.Cooler.__stabilize_temperature`
        for holding press event info.

    """

    def __init__(self, fan_pins):
        """Initialization method of :class:`t_system.stand.Button` class.

        Args:
            fan_pins (list):       	    GPIO pins to use for fans.
        """

        self.fans = []

        for pin in fan_pins:
            fan = Fan(pin)
            fan.start(25)

            self.fans.append(fan)

        self.min_temperature = 45
        self.max_temperature = 80

        self.stop_thread = False
        self.cooling_thread = threading.Thread(target=self.__stabilize_temperature, args=(lambda: self.stop_thread,))

    def start(self):
        """Method to start of the asynchronous cooling process of cooler.
        """

        if not self.cooling_thread.is_alive():
            self.cooling_thread = threading.Thread(target=self.__stabilize_temperature, args=(lambda: self.stop_thread,))
            self.cooling_thread.start()

    def __stabilize_temperature(self, stop_thread):
        """Method to provide asynchronous temperature control point for running fans by the temperature.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
        """

        from gpiozero import CPUTemperature
        cpu = CPUTemperature()

        while True:
            temperature = float(cpu.temperature)

            for fan in self.fans:
                if temperature <= 45:
                    fan.change_speed(0)
                elif temperature <= 75:
                    fan.change_speed(100)
                else:
                    fan.change_speed(self.__temperature_to_percent(temperature))

            if stop_thread():
                break

            time.sleep(1.5)

    def __temperature_to_percent(self, temperature):
        """Method to convert temperature to percentage.

        Args:
            temperature (float):     The temperature value of the cpu. Taken as celsius.
        """

        return ((temperature - self.min_temperature) / (self.max_temperature - self.min_temperature)) * 100

    def stop(self):
        """Method to provide stop the GPIO.PWM service that is reserved the cooler fans.
        """

        if self.cooling_thread.is_alive():
            self.stop_thread = True
            self.cooling_thread.join()

        for fan in self.fans:
            fan.stop()
            fan.gpio_cleanup()


class Stand:
    """Class to define tracking system's stand interface.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.stand.Stand` class.

        Args:
            args:                       Command-line arguments.
        """

        from t_system.remote_ui import RemoteUI

        self.remote_ui = RemoteUI(args)

        self.network_connector = NetworkConnector(args)
        self.access_point = AccessPoint(args)

        self.static_ip = args["static_ip"]

        self.red_led = Led(args["stand_gpios"][0])
        self.green_led = Led(args["stand_gpios"][1])

        self.cooler = Cooler([args["stand_gpios"][2]])

        self.stop_thread = False

    def run(self):
        """The top-level method to managing members of stand interface.
        """

        self.cooler.start()

        is_connected_to_network = self.network_connector.is_connected_to_network()

        if not is_connected_to_network:
            is_connected_to_network = self.network_connector.connect()

        if not is_connected_to_network:
            self.access_point.start()

        try:
            self.remote_ui.run()
        except KeyboardInterrupt:
            # TODO: After keyboard interrupt access point still active. so restarting the t_system is being corrupted. Following solution is not working. Fix this.
            if self.access_point.is_working():
                self.access_point.stop()

    def blink_led(self, stop_thread, led, delay_time=None):
        """Method to blinking the LEDs with different on/off combinations.

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
        """Method to turning off the all led lights.
        """
        self.red_led.off()
        self.green_led.off()

    @staticmethod
    def start_thread(job, job_args, working_threads):
        """Method to starting new thread.

        Args:
            job:                        The function that is going to applied with multiprocessing.
            job_args (tuple):           Arguments of the job.
            working_threads (list):     List of working threads.
        """

        thread = threading.Thread(target=job, args=job_args)
        working_threads.append(thread)
        thread.start()

    def __terminate_threads(self, working_threads):
        """Method to killing existing threads/running modes.

        Args:
            working_threads (list):     List of working threads.
        """

        self.stop_thread = True
        for worker in working_threads:  # For checking the existing thread.
            worker.join()
        working_threads.clear()
        self.stop_thread = False

    def release_members(self):
        """Method to releasing camera, stop sending signals and clean up the gpio pins.
        """

        self.red_led.gpio_cleanup()
        self.green_led.gpio_cleanup()

        self.cooler.stop()
