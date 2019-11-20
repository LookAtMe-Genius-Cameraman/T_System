#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: locking_system
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's Target Locking System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import threading

from math import pi

from t_system.motion.locking_system.collimator import Collimator

from t_system import arm
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class LockingSystem:
    """Class to define a target locking system of the t_system's motion ability.

        This class provides necessary initiations and a function named :func:`t_system.motion.LockingSystem.lock`
        for the provide move of servo motor during locking to the target.

    """

    def __init__(self, args, frame_w_h, decider=None, init_angles=(pi/2, pi/3)):
        """Initialization method of :class:`t_system.motion.LockingSystem` class.

        Args:
                args:                   Command-line arguments.
                frame_w_h (tuple):      The tuple that is contain width and height info of the vision limits.
                decider:                decider object of Decider class.
                init_angles:       	    Initialization angle values for pan and tilt's servo motors as radian unit.
        """

        self.frame_width = frame_w_h[0]
        self.frame_height = frame_w_h[1]

        self.frame_middle_x = self.frame_width / 2 - 1
        self.frame_middle_y = self.frame_height / 2 - 1

        self.decider = decider
        self.current_k_fact = 0.01

        self.pan = Collimator((args["ls_gpios"][0], args["ls_channels"][0]), self.frame_width, init_angles[0], False, use_ext_driver=args["ext_servo_driver"])      # pan means rotate right and left ways.
        self.tilt = Collimator((args["ls_gpios"][1], args["ls_channels"][1]), self.frame_height, init_angles[1], False, use_ext_driver=args["ext_servo_driver"])   # tilt means rotate up and down ways.

        self.current_target_obj_width = 0

        self.locker = None
        self.lock = None
        self.check_error = None
        self.get_physically_distance = None

        self.scan_thread_stop = False

        self.load_locker(args["AI"], args["non_moving_target"], args["arm_expansion"], init_angles)

    def load_locker(self, ai, non_moving_target, arm_expansion, current_angles):
        """Method to set locking system's locker as given AI and target object status parameters.

        Args:
                ai (str):                       AI type that will using during locking the target.
                non_moving_target (bool):       Non-moving target flag.
                arm_expansion (bool):           Flag for the loading locker as expansion of the T_System's robotic arm.
                current_angles (list):          Current angles of the target locking system's collimators.
        """
        if arm_expansion is False:
            self.pan.restart(current_angles[0])
            self.tilt.restart(current_angles[1])

        if ai == "official_ai":
            self.locker = self.OfficialAILocker(self)
            self.lock = self.locker.lock
            self.check_error = self.locker.check_error
            self.get_physically_distance = self.locker.get_physically_distance
        elif non_moving_target or arm_expansion:
            self.locker = self.ArmExpansionLocker(self)
            self.lock = self.locker.lock
            self.get_physically_distance = self.locker.get_physically_distance
        else:
            self.locker = self.RegularLocker(self)
            self.lock = self.locker.lock
            self.get_physically_distance = self.locker.get_physically_distance

        return [self.tilt.current_angle, self.pan.current_angle]

    class OfficialAILocker:
        """Class to define a official AI method of the t_system's motion ability.

            This class provides necessary initiations and a function named
            :func:`t_system.motion.LockingSystem.OfficialAILocker.lock`
            for the provide move of servo motor during locking to the target.
        """

        def __init__(self, locking_system):
            """Initialization method of :class:`t_system.motion.LockingSystem.OfficialAILocker` class.

            Args:
                    locking_system:         The LockingSystem Object.
            """

            self.root_system = locking_system
            self.decider = self.root_system.decider

            self.current_k_fact = 0.01
            self.current_target_obj_width = 0

            if arm.is_expanded():
                self.root_system.pan.restart()
                self.root_system.tilt.restart()

        def lock(self, x, y, w, h):
            """Method for locking to the target in the frame.

            Args:
                    x           :       	 the column number of the top left point of found object from haarcascade.
                    y           :       	 the row number of the top left point of found object from haarcascade.
                    w           :       	 the width of found object from haarcascade.
                    h           :       	 the height of found object from haarcascade.
            """

            # obj_width is equal to w
            self.current_target_obj_width = w
            self.current_k_fact = self.__get_k_fact(w)

            self.root_system.pan.move(x, x + w, w, self.current_k_fact)
            self.root_system.tilt.move(y, y + h, w, self.current_k_fact)

        def check_error(self, ex, ey, ew, eh):
            """Method for checking error during locking to the target in the frame.

            Args:
                    ex           :       	 the column number of the top left point of found object from haarcascade.
                    ey           :       	 the row number of the top left point of found object from haarcascade.
                    ew           :       	 the width of found object from haarcascade.
                    eh           :       	 the height of found object from haarcascade.
            """

            err_rate_pan = float(self.root_system.pan.current_dis_to_des(ex, ex + ew) / self.root_system.pan.get_previous_dis_to_des()) * 100
            err_rate_tilt = float(self.root_system.tilt.current_dis_to_des(ey, ey + eh) / self.root_system.tilt.get_previous_dis_to_des()) * 100

            self.decider.decision(self.current_target_obj_width, err_rate_pan, True)
            self.decider.decision(self.current_target_obj_width, err_rate_tilt, True)

        def __get_k_fact(self, obj_width):
            """Method to getting necessary k_fact by given object width.

            Args:
                obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            """

            return self.decider.decision(obj_width)

        def get_physically_distance(self, obj_width):
            """Method to provide return the tracking object's physically distance value.
            """

            return obj_width / self.current_k_fact  # physically distance is equal to obj_width / k_fact.

    class RegularLocker:
        """Class to define a basic object tracking method of the t_system's motion ability.

            This class provides necessary initiations and a function named
            :func:`t_system.motion.LockingSystem.RegularLocker.lock`
            for the provide move of servo motor during locking to the target.

        """

        def __init__(self, locking_system):
            """Initialization method of :class:`t_system.motion.LockingSystem.RegularLocker` class.

            Args:
                    locking_system:         The LockingSystem Object.
            """

            self.root_system = locking_system

        def lock(self, x, y, w, h):
            """Method for locking to the target in the frame.

            Args:
                    x           :       	 the column number of the top left point of found object from haarcascade.
                    y           :       	 the row number of the top left point of found object from haarcascade.
                    w           :       	 the width of found object from haarcascade.
                    h           :       	 the height of found object from haarcascade.
            """

            precision_ratio = 0.2
            obj_middle_x = x + w / 2  # middle point's x axis coordinate of detected object
            obj_middle_y = y + h / 2  # middle point's y axis coordinate of detected object

            if obj_middle_x < self.root_system.frame_middle_x - self.root_system.frame_middle_x * precision_ratio:
                self.root_system.pan.move(False, True)  # last parameter True is for the clockwise and False is can't clockwise direction
            elif obj_middle_x > self.root_system.frame_middle_x + self.root_system.frame_middle_x * precision_ratio:
                self.root_system.pan.move(False, False)  # First parameter is the stop flag.
            else:
                self.root_system.pan.move(True, False)

            if obj_middle_y < self.root_system.frame_middle_y - self.root_system.frame_middle_y * precision_ratio:
                self.root_system.tilt.move(False, True)  # last parameter True is for the clockwise and False is can't clockwise direction
            elif obj_middle_y > self.root_system.frame_middle_y + self.root_system.frame_middle_y * precision_ratio:
                self.root_system.tilt.move(False, False)  # First parameter is the stop flag.
            else:
                self.root_system.tilt.move(True, False)

        @staticmethod
        def get_physically_distance(obj_width):
            """Method to provide return the tracking object's physically distance value.
            """
            kp = 28.5823  # gain rate with the width of object and physically distance.
            return obj_width * kp  # physically distance is equal to obj_width * kp in px unit. 1 px length is equal to 0.164 mm

    class ArmExpansionLocker:
        """Class to define a locker as an extension of robotic arm of the t_system's motion ability. For focused non-moving point tracking or emotion showing.

            This class provides necessary initiations and a function named
            :func:`t_system.motion.LockingSystem.ArmExpansionLocker.lock`
            for the provide move of servo motor during locking to the target.
        """

        def __init__(self, locking_system):
            """Initialization method of :class:`t_system.motion.LockingSystem.ArmExpansionLocker` class.

            Args:
                    locking_system:         The LockingSystem Object.
            """

            self.root_system = locking_system

            if not arm.is_expanded():
                self.root_system.stop()
                self.root_system.gpio_cleanup()

        def lock(self, x, y, w, h):
            """Method for locking to the target in the frame.

            Args:
                    x           :       	 the column number of the top left point of found object from haarcascade.
                    y           :       	 the row number of the top left point of found object from haarcascade.
                    w           :       	 the width of found object from haarcascade.
                    h           :       	 the height of found object from haarcascade.
            """
            pass

        @staticmethod
        def get_physically_distance(obj_width):
            """Method to provide return the tracking object's physically distance value.
            """
            kp = 28.5823  # gain rate with the width of object and physically distance.
            return obj_width * kp  # physically distance is equal to obj_width * kp in px unit. 1 px length is equal to 0.164 mm

    def scan(self, stop):
        """Method to scan around for detecting the object that will be locked before lock process.

        Args:
                stop:       	         Stop flag of the tread about terminating it outside of the function's loop.
        """

        self.scan_thread_stop = stop

        threading.Thread(target=self.__scan).start()

    def __scan(self):
        """Method to cycle collimator respectively clockwise and can't clockwise.
        """

        precision_ratio = 0.95

        while not self.scan_thread_stop:
            while not self.tilt.current_angle >= self.tilt.max_angle * precision_ratio and not self.scan_thread_stop:
                self.tilt.move(False, 5, 30)

                while not self.pan.current_angle >= self.pan.max_angle * precision_ratio and not self.scan_thread_stop:
                    self.pan.move(False, 2, 30)

                self.tilt.move(False, 5, 30)

                while not self.pan.current_angle <= self.pan.min_angle / precision_ratio and not self.scan_thread_stop:
                    self.pan.move(True, 2, 30)

            while not self.tilt.current_angle <= self.tilt.min_angle / precision_ratio and not self.scan_thread_stop:
                self.tilt.move(True, 5, 30)

                while not self.pan.current_angle >= self.pan.max_angle * precision_ratio and not self.scan_thread_stop:
                    self.pan.move(False, 2, 30)

                self.tilt.move(True, 5, 30)

                while not self.pan.current_angle <= self.pan.min_angle / precision_ratio and not self.scan_thread_stop:
                    self.pan.move(True, 2, 30)

        self.scan_thread_stop = False

    def stop(self):
        """Method to provide stop the GPIO.PWM services that are reserved for the locking system's servo motors.
        """
        self.pan.stop()
        self.tilt.stop()

    def gpio_cleanup(self):
        """Method to provide clean the GPIO pins that are reserved for the locking system's servo motors
        """
        self.pan.gpio_cleanup()
        self.tilt.gpio_cleanup()
