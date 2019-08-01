#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: locking_system
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's Target Locking System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from math import pi

from t_system.motion.locking_system.collimator import Collimator


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

        self.pan = Collimator(args["ls_gpios"][0], self.frame_width, init_angles[0])      # pan means rotate right and left ways.
        self.tilt = Collimator(args["ls_gpios"][1], self.frame_height, init_angles[1], False)   # tilt means rotate up and down ways.

        self.current_target_obj_width = 0

        self.check_error = None
        self.get_physically_distance = None

        if args["AI"] == "official_ai":
            self.locker = self.OfficialAILocker(self)
            self.lock = self.locker.lock
            self.check_error = self.locker.check_error
            self.get_physically_distance = self.locker.get_physically_distance
        elif args["non_moving_target"]:
            self.locker = self.NonMovingTargetLocker(self)
            self.lock = self.locker.lock
            self.get_physically_distance = self.locker.get_physically_distance
        else:
            self.locker = self.RegularLocker(self)
            self.lock = self.locker.lock
            self.get_physically_distance = self.locker.get_physically_distance

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
            self.decider = locking_system.decider

            self.current_k_fact = 0.01
            self.current_target_obj_width = 0

        def lock(self, x, y, w, h):
            """The high-level method for locking to the target in the frame.

            Args:
                x           :       	 the column number of the top left point of found object from haarcascade.
                y           :       	 the row number of the top left point of found object from haarcascade.
                w           :       	 the width of found object from haarcascade.
                h           :       	 the height of found object from haarcascade.
            """

            # obj_width is equal to w
            self.current_target_obj_width = w
            self.current_k_fact = self.get_k_fact(w)

            self.root_system.pan.move(x, x + w, w, self.current_k_fact)
            self.root_system.tilt.move(y, y + h, w, self.current_k_fact)

        def check_error(self, ex, ey, ew, eh):
            """The high-level method for checking error during locking to the target in the frame.

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

        def get_k_fact(self, obj_width):
            """The low-level method to getting necessary k_fact by given object width.

            Args:
                obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            """

            return self.decider.decision(obj_width)

        def get_physically_distance(self, obj_width):
            """The low-level method to provide return the tracking object's physically distance value.
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
            """The high-level method for locking to the target in the frame.

            Args:
                x           :       	 the column number of the top left point of found object from haarcascade.
                y           :       	 the row number of the top left point of found object from haarcascade.
                w           :       	 the width of found object from haarcascade.
                h           :       	 the height of found object from haarcascade.
            """

            precision_ratio = 0.10
            obj_middle_x = x + w / 2  # middle point's x axis coordinate of detected object
            obj_middle_y = y + h / 2  # middle point's y axis coordinate of detected object

            if obj_middle_x < self.root_system.frame_middle_x - self.root_system.frame_middle_x * precision_ratio:
                self.root_system.pan.move(False, True)  # last parameter True is for the clockwise and False is can't clockwise direction
            elif obj_middle_x > self.root_system.frame_middle_x + self.root_system.frame_middle_x * precision_ratio:
                self.root_system.pan.move(False, False)  # First parameter is the stop flag.
            else:
                self.root_system.pan.move(True, False)

            if obj_middle_y < self.root_system.frame_middle_y - self.root_system.frame_middle_y * precision_ratio:
                self.root_system.tilt.move(False, True)  # last parameter True is for the clockwise and False is can't clockwise directionx
            elif obj_middle_y > self.root_system.frame_middle_y + self.root_system.frame_middle_y * precision_ratio:
                self.root_system.tilt.move(False, False)  # First parameter is the stop flag.
            else:
                self.root_system.tilt.move(True, False)

        @staticmethod
        def get_physically_distance(obj_width):
            """The low-level method to provide return the tracking object's physically distance value.
            """
            kp = 28.5823  # gain rate with the width of object and physically distance.
            return obj_width * kp  # physically distance is equal to obj_width * kp in px unit. 1 px length is equal to 0.164 mm

    class NonMovingTargetLocker:
        """Class to define a focused point tracking method of the t_system's motion ability.

            This class provides necessary initiations and a function named
            :func:`t_system.motion.LockingSystem.NonMovingTargetLocker.lock`
            for the provide move of servo motor during locking to the target.
        """

        def __init__(self, locking_system):
            """Initialization method of :class:`t_system.motion.LockingSystem.NonMovingTargetLocker` class.

            Args:
                locking_system:         The LockingSystem Object.
            """

            self.root_system = locking_system

        def lock(self, x, y, w, h):
            """The high-level method for locking to the target in the frame.

            Args:
                x           :       	 the column number of the top left point of found object from haarcascade.
                y           :       	 the row number of the top left point of found object from haarcascade.
                w           :       	 the width of found object from haarcascade.
                h           :       	 the height of found object from haarcascade.
            """
            pass

        @staticmethod
        def get_physically_distance(obj_width):
            """The low-level method to provide return the tracking object's physically distance value.
            """
            kp = 28.5823  # gain rate with the width of object and physically distance.
            return obj_width * kp  # physically distance is equal to obj_width * kp in px unit. 1 px length is equal to 0.164 mm

    def stop(self):
        """The low-level method to provide stop the GPIO.PWM services that are reserved for the locking system's servo motors.
        """
        self.pan.stop()
        self.tilt.stop()

    def gpio_cleanup(self):
        """The low-level method to provide clean the GPIO pins that are reserved for the locking system's servo motors
        """
        self.pan.gpio_cleanup()
        self.tilt.gpio_cleanup()
