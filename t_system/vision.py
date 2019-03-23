#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: vision
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's vision ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import time  # Time access and conversions
import inspect  # Inspect live objects
import os  # Miscellaneous operating system interfaces


from picamera.array import PiRGBArray

import cv2

from t_system.motor import Motor
from t_system.motor import calc_ellipsoidal_angle
from t_system.decision import Decider


T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


class Vision():
    """Class to define a vision of tracking system..

    This class provides necessary initiations and a function named :func:`t_system.Vision.rtime_detect`
    as the loop for each camera frames.

    """

    def __init__(self, args, camera, resolution=(320, 240), framerate=32):
        """Initialization method of :class:`t_system.Vision` class.

        Args:
                camera:       	        Camera object from PiCamera.
                resolution:    	        rPi camera's resolution data.
                framerate:              rPi camera's framerate data.

        """
        if not args["cascadefile"]:
            ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/frontalface_default.xml"
            self.decider = Decider()
        else:
            ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + args["cascadefile"] + ".xml"
            self.decider = Decider(args["cascadefile"])

        self.servo_pan = Motor(17, self.decider)      # pan means rotate right and left ways.
        self.servo_tilt = Motor(14, self.decider, 4.5, False)  # tilt means rotate up and down ways.

        self.show_stream = args["show_stream"]  # 'show-stream' argument automatically converted this type.
        self.augmented = args["augmented"]

        self.camera = camera
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        # self.camera.start_preview()

        self.rawCapture = PiRGBArray(camera, size=resolution)
        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)
        (self.frame_width, self.frame_height) = resolution

        self.mqtt_receimitter = None

        # allow the camera to warmup
        time.sleep(0.1)

    def detect_track(self, stop_thread, format="bgr"):
        """The top-level method to real time object detection.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text

            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.equalizeHist(gray)

            objects = self.object_cascade.detectMultiScale(gray, 1.3, 5)

            if not len(objects) == 1:
                pass
            else:
                for (x, y, w, h) in objects:

                    if self.show_stream or not self.augmented:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    self.servo_pan.move(x, x + w, self.frame_width)
                    self.servo_tilt.move(y, y + h, self.frame_height)

                    time.sleep(0.1)  # allow the servos to complete the moving.

            if self.show_stream or not self.augmented:
                # show the frame
                cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                # print("thread killed")
                break

    def learn(self, stop_thread, format="bgr"):
        """The top-level method to learn how to track objects.

         Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text

            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.equalizeHist(gray)

            objects = self.object_cascade.detectMultiScale(gray, 1.3, 5)

            if not len(objects) == 1:
                pass
            else:
                for (x, y, w, h) in objects:

                    if self.show_stream or not self.augmented:
                        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    obj_width_pan = self.servo_pan.move(x, x + w, self.frame_width)
                    obj_width_tilt = self.servo_tilt.move(y, y + h, self.frame_height)

                    time.sleep(0.5)  # allow the camera to capture after moving.

                    self.rawCapture.truncate(0)  # for emptying arrays for capturing frame again.

                    self.camera.capture(self.rawCapture, format=format)
                    error_check_image = self.rawCapture.array
                    error_check_gray = cv2.cvtColor(error_check_image, cv2.COLOR_BGR2GRAY)
                    # gray = cv2.equalizeHist(gray)

                    objects_after_move = self.object_cascade.detectMultiScale(error_check_gray, 1.3, 5)
                    if not len(objects_after_move) == 1:
                        pass
                    else:
                        for (x, y, w, h) in objects_after_move:

                            if self.show_stream or not self.augmented:
                                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                            err_rate_pan = float(self.servo_pan.current_dis_to_des(x, x+w, self.frame_width) / self.servo_pan.get_previous_dis_to_des()) * 100
                            err_rate_tilt = float(self.servo_tilt.current_dis_to_des(y, y+h, self.frame_height) / self.servo_tilt.get_previous_dis_to_des()) * 100

                            self.decider.decision(obj_width_pan, err_rate_pan, True)
                            self.decider.decision(obj_width_tilt, err_rate_tilt, True)

            if self.show_stream or not self.augmented:
                # show the frame
                cv2.imshow("Frame", image)

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                # print("thread killed")
                break

    def security(self, stop_thread,  format="bgr"):
        """The top-level method to provide the security via scanning and taking photos.

         Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        import threading

        global thread_of_scan
        global thread_of_stream
        is_first_run = True

        while True:
            if is_first_run or stop_thread():
                if not stop_thread():
                    thread_of_scan = threading.Thread(target=self.scan, args=(stop_thread, 3))
                    thread_of_stream = threading.Thread(target=self.stream, args=(stop_thread, format))

                    thread_of_scan.start()
                    thread_of_stream.start()
                else:
                    # print("thread killed")

                    thread_of_scan.join()
                    thread_of_stream.join()
                    break
                is_first_run = False
            time.sleep(0.5)  # for relieve the cpu.

    def scan(self, stop_thread, resolution=3):
        """The top-level method to provide the scanning around for security mode of T_System.

        Args:
                stop_thread:   	       Stop flag of the tread about terminating it outside of the function's loop.
                resolution:            angle's step width between 0 - 180 degree.
        """
        while True:
            if stop_thread():
                break
            for angle in range(0, 180, resolution):
                if stop_thread():
                    break
                self.servo_pan.angular_move(float(angle), 180.0)
                angle_for_ellipse_move = calc_ellipsoidal_angle(float(angle) - 90, 180.0, 75.0)  # 75 degree is for physical conditions.
                self.servo_tilt.angular_move(angle_for_ellipse_move, 75.0)
                time.sleep(0.1)

            for angle in range(180, 0, resolution * -1):
                if stop_thread():
                    break
                self.servo_pan.angular_move(float(angle), 180.0)
                angle_for_ellipse_move = calc_ellipsoidal_angle(float(angle) - 90, 180.0, 75.0)
                self.servo_tilt.angular_move(angle_for_ellipse_move, 75.0)
                time.sleep(0.1)

    def stream(self, stop_thread, format="bgr"):
        """The top-level method to provide the video stream for security mode of T_System.

        Args:
                stop_thread:   	       Stop flag of the tread about terminating it outside of the function's loop.
                resolution:            angle's step width between 0 - 180 degree.
        """
        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text

            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.equalizeHist(gray)

            # SECURITY MODE CAN BE TAKING PHOTOGRAPHS AS DIFFERENT FROM learn AND detect_track FUNCTIONS.
            # objects = self.object_cascade.detectMultiScale(gray, 1.3, 5)
            #
            # if not len(objects) == 1:
            #     pass
            # else:
            #     for (x, y, w, h) in objects:
            #         if self.show_stream or not self.augmented:
            #             cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if self.show_stream or not self.augmented:
                # show the frame
                cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                break

        # if loop end, the scan process will be terminated.

    def change_tracked_thing(self, file):
        """The top-level method to changing tracking objects.

         Args:
                file:       	        The haarcascade trained xml file.
        """
        ccade_xml_file = T_SYSTEM_PATH + "/" + file

        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)
        self.decider.set_db(file)

    def set_mqtt_receimitter(self, mqtt_receimitter):
        """The top-level method to set mqtt_receimitter object for publishing and subscribing data echos.

         Args:
                mqtt_receimitter:          transmit and receive data function for mqtt communication
        """
        self.mqtt_receimitter = mqtt_receimitter
