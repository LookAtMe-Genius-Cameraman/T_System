#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: vision
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's vision ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from t_system.motion import Motion
from t_system.decision import Decider

servo_pan = Motion(17)
servo_tilt = Motion(14, 5)
decider = Decider()


class Vision():
    """Class to define a vision of tracking system..

        This class provides necessary initiations and a function named :func:`t_system.Vision.rtime_detect`
        as the loop for each camera frames.

        """

    def __init__(self, camera, ccade_xml_file, resolution=(320, 240), framerate=32):
        """Initialization method of :class:`t_system.Vision` class.

        Args:
                camera:       	        Camera object from PiCamera.
                resolution:    	        rPi camera's resolution data.
                framerate:              rPi camera's framerate data.

        Keyword Args:
                ccade_xml_file (str):      Trained cascade .xml file.
        """

        self.camera = camera
        self.camera.resolution = resolution
        self.camera.framerate = framerate

        self.rawCapture = PiRGBArray(camera, size=resolution)
        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)
        (self.frame_width, self.frame_height) = resolution
        # allow the camera to warmup
        time.sleep(0.1)

    def rtime_detect(self, format="bgr"):
        """The top-level method to real time object detection.

            Args:
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
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    obj_width_pan = servo_pan.move(x, x+w, self.frame_width)
                    obj_width_tilt = servo_tilt.move(y, y+h, self.frame_height)

                    time.sleep(0.1)  # allow the camera to capture after moving.

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

                            err_rate_pan = float(servo_pan.current_dis_to_des(x, x+w, self.frame_width) / servo_pan.get_previous_dis_to_des()) * 100
                            err_rate_tilt = float(servo_tilt.current_dis_to_des(y, y+h, self.frame_height) / servo_tilt.get_previous_dis_to_des()) * 100

                            decider.decision(obj_width_pan, err_rate_pan, True)
                            decider.decision(obj_width_tilt, err_rate_tilt, True)

            # show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

