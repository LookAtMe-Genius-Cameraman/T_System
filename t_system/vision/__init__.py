#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: vision
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's vision ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import time  # Time access and conversions
import cv2
import face_recognition
import pickle
import numpy as np
import threading
import json

from math import sqrt
from multipledispatch import dispatch
from picamera import PiCamera
from picamera.array import PiRGBArray

from t_system.motion.locking_system import LockingSystem
from t_system.motion import calc_ellipsoidal_angle
from t_system.decision import Decider
from t_system.audition import Hearer
from t_system.recordation import Recorder

from t_system.high_tech_aim import Aimer
from t_system import T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class Vision:
    """Class to define a vision of tracking system..

    This class provides necessary initiations and functions named :func:`t_system.vision.Vision.detect_track`
    as the loop for each camera frames for tracking mode, named :func:`t_system.vision.Vision.learn` as the
    learning ability and :func:`t_system.vision.Vision.security` as the security mode.

    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.vision.Vision` class.

        Args:
                args:                   Command-line arguments.
        """

        self.config_file = f'{T_SYSTEM_PATH}/vision/vision_config.json'

        with open(self.config_file) as conf_file:
            conf_file_json = json.load(conf_file)
            self.tracker_types = conf_file_json["tracker_types"]  # config file returns the tracker type list.
            self.target_mark_types = conf_file_json["target_mark_types"]  # config file returns the mark type dict.

        self.detection_model = args["detection_model"]

        if self.detection_model == "haarcascade":
            self.detect_things = self.__detect_with_haarcascade
        else:
            self.detect_things = self.__detect_with_hog_or_cnn

        if args['use_tracking_api']:
            self.detect_track = self.__d_t_with_cv_ta
        else:
            self.detect_track = self.__d_t_without_cv_ta

        # Specify the tracker type
        self.tracker_type = args["tracker_type"]

        self.no_recognize = args["no_recognize"]

        if not self.no_recognize:
            self.recognition_data = self.__get_recognition_data(args["encoding_file"])
            self.track = self.__track_with_recognizing
        else:
            self.track = self.__track_without_recognizing

        self.hearer = Hearer(args)
        # self.hearer = None

        resolution = (args["resolution"][0], args["resolution"][1])
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = args["framerate"]
        self.camera.rotation = 240

        self.recorder = Recorder(args["record_formats"], self.camera, self.hearer)

        self.raw_capture = PiRGBArray(self.camera, size=resolution)

        ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + args["cascade_file"] + ".xml"
        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)

        (self.frame_width, self.frame_height) = resolution

        self.decider = None
        if args["AI"] == "official_ai":
            self.decider = Decider(args["cascade_file"])

        self.target_locker = LockingSystem(args, resolution, self.decider)

        self.aimer = Aimer()

        self.show_stream = args["show_stream"]  # 'show-stream' argument automatically converted this type.
        self.mark_object = self.__get_mark_object(args["found_object_mark"])

        self.record = args["record"]
        self.record_path = ""
        self.record_name = ""

        self.augmented = False
        if args["interface"] == "augmented":
            self.augmented = True

        self.mqtt_receimitter = None
        
        self.current_frame = np.zeros(shape=(self.frame_height, self.frame_width))

        self.stop_thread = False
        self.active_threads = []

        self.is_watching = False

        # Allow the camera to warm up
        time.sleep(0.1)

    def watch(self, stop_thread, format="bgr", caller="security"):
        """The top-level method to provide the video stream for security mode of T_System.

        Args:
                stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.
                format (str):  	        Color space format.
                caller (str): 	        The method that calls the stream.
        """

        self.is_watching = True

        if self.record:
            self.recorder.start(caller)

        logger.debug("stream starting with capture_continuous")

        for frame in self.camera.capture_continuous(self.raw_capture, format=format, use_video_port=True):

            self.current_frame = frame.array

            self.__show_frame(self.current_frame)
            self.__truncate_stream()

            if self.__check_loop_ended(stop_thread):
                break

        if self.record:
            self.stop_recording()

        self.is_watching = False

    def watch_and(self, task):
        """Method to provide starting watching ability of the around of Vision and accordingly starting given task.

        Args:
                task:             	    Task for the seer. Either `learn`, `track` or `secure`.
        """

        watch_thread = threading.Thread(target=self.watch, args=(lambda: self.stop_thread, "bgr", task))
        self.active_threads.append(watch_thread)
        watch_thread.start()

        if task == "learn":
            learn_thread = threading.Thread(target=self.learn, args=(lambda: self.stop_thread,))
            self.active_threads.append(learn_thread)
            learn_thread.start()

        elif task == "track":
            track_thread = threading.Thread(target=self.detect_track, args=(lambda: self.stop_thread,))
            track_thread.start()
            self.active_threads.append(track_thread)

        elif task == "secure":
            secure_thread = threading.Thread(target=self.scan, args=(lambda: self.stop_thread, 3))
            secure_thread.start()
            self.active_threads.append(secure_thread)

    def __d_t_without_cv_ta(self, stop_thread, format='bgr'):
        """Method to provide detecting and tracking objects without using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        self.__detect_initiate()

        last_frame = np.zeros(shape=(self.frame_height, self.frame_width))

        while True:
            if last_frame.any() != self.current_frame.any():

                last_frame = self.current_frame

                rgb, detected_boxes = self.detect_things(last_frame)
                reworked_boxes = self.__relocate_detected_coords(detected_boxes)

                if not self.no_recognize:
                    names = self.__recognize_things(rgb, detected_boxes)
                else:
                    names = None

                self.track(last_frame, reworked_boxes, names)

                self.__show_frame(last_frame)
                # print("frame showed!")
            if self.__check_loop_ended(stop_thread):
                break

    def __d_t_with_cv_ta(self, stop_thread, format='bgr'):
        """Method to provide detecting and tracking objects with using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        tracked_boxes = []  # this became array.  because of overriding.
        names = []

        multi_tracker = cv2.MultiTracker_create()

        rgb, detected_boxes = self.__detect_initiate()

        found_count = 0
        d_t_failure_count = 0
        use_detection = 0

        last_frame = np.zeros(shape=(self.frame_height, self.frame_width))

        while True:
            if last_frame.any() != self.current_frame.any():

                last_frame = self.current_frame

                if len(detected_boxes) > len(tracked_boxes):

                    if not self.no_recognize:
                        names = self.__recognize_things(rgb, detected_boxes)
                    else:
                        names = None

                    last_frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

                    # Create MultiTracker object
                    multi_tracker = cv2.MultiTracker_create()

                    # Initialize MultiTracker
                    for box in detected_boxes:
                        # box[3] is x,
                        # box[0] is y,
                        # box[1] is x + w,
                        # box[2] is y + h.
                        reworked_box = box[3], box[0], box[1] - box[3], box[2] - box[0]

                        multi_tracker.add(self.__create_tracker_by_name(), last_frame, reworked_box)
                    found_count += 1

                if use_detection >= 3:
                    rgb, detected_boxes = self.detect_things(last_frame)
                    use_detection = 0

                use_detection += 1

                # Start timer
                timer = cv2.getTickCount()

                # get updated location of objects in subsequent frames
                is_tracking_success, tracked_boxes = multi_tracker.update(last_frame)

                if not len(detected_boxes) >= len(tracked_boxes):
                    d_t_failure_count += 1
                else:
                    d_t_failure_count = 0

                # Calculate Frames per second (FPS)
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

                if is_tracking_success and d_t_failure_count < 5:

                    self.track(last_frame, tracked_boxes, names)

                elif not is_tracking_success or d_t_failure_count >= 5:
                    # Tracking failure
                    cv2.putText(last_frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    tracked_boxes = []  # for clearing tracked_boxes list.

                # # Display tracker type on frame
                # cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
                #
                # # Display FPS on frame
                # cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

                self.__show_frame(last_frame)
                # self.__truncate_stream()

            if self.__check_loop_ended(stop_thread):
                break

    def __track_without_recognizing(self, frame, boxes, names):
        """Method to track the objects without recognize them, for detect_track methods.

        Args:
                frame:  	            Frame matrix in rgb format.
                boxes:       	        Tuple variable of locations of detected objects.
                names:       	        Names of the recognized objects. A person or just an object.
        """

        if len(boxes) == 1:

            for (x, y, w, h) in boxes:
                physically_distance = self.target_locker.get_physically_distance(w)  # for calculating the just about physically distance of object.
                radius = int(sqrt(w * w + h * h) / 2)

                self.target_locker.lock(x, y, w, h)

                if (self.show_stream and self.augmented) or self.show_stream:
                    self.mark_object(frame, x, y, w, h, radius, physically_distance, (255, 0, 0), 2)

            # time.__sleep(0.1)  # Allow the servos to complete the moving.

    def __track_with_recognizing(self, frame, boxes, names):
        """Method to track the objects with recognize them, for detect_track methods.

        Args:
                frame:  	            Frame matrix in rgb format.
                boxes:       	        Tuple variable of locations of detected objects.
                names:       	        Names of the recognized objects. A person or just an object.
        """

        for (x, y, w, h), name in zip(boxes, names):

            physically_distance = self.target_locker.get_physically_distance(w)  # for calculating the just about physically distance of object.
            radius = int(sqrt(w * w + h * h) / 2)

            if name == "Unknown":
                if (self.show_stream and self.augmented) or self.show_stream:
                    frame = self.aimer.mark_rotating_arcs(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)
            else:
                self.target_locker.lock(x, y, w, h)

                if (self.show_stream and self.augmented) or self.show_stream:
                    self.mark_object(frame, x, y, w, h, radius, physically_distance, (255, 0, 0), 2)

        # time.__sleep(0.1)  # Allow the servos to complete the moving.

    def learn(self, stop_thread, format="bgr"):
        """The top-level method to learn how to track objects.

         Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        self.__detect_initiate()

        last_frame = np.zeros(shape=(self.frame_height, self.frame_width))

        while True:
            if last_frame.any() != self.current_frame.any():

                last_frame = self.current_frame

                rgb, detected_boxes = self.detect_things(last_frame)
                # names = self.__recognize_things(rgb, detected_boxes)
                reworked_boxes = self.__relocate_detected_coords(detected_boxes)

                if not len(reworked_boxes) == 1:
                    # self.__show_frame(self.current_frame)
                    pass
                else:
                    for (x, y, w, h) in reworked_boxes:

                        if (self.show_stream and self.augmented) or self.show_stream:
                            self.mark_object(last_frame, x, y, w, h, 30, 50, (255, 0, 0), 2)
                        obj_width = w
                        # obj_area = w * h  # unit of obj_width is px ^ 2.

                        self.target_locker.lock(x, y, w, h)

                        # time.__sleep(0.2)  # allow the camera to capture after moving.

                        while True:
                            if last_frame.any() != self.current_frame.any():
                                last_frame = self.current_frame

                                rgb, detected_boxes = self.detect_things(last_frame)
                                # names = self.__recognize_things(rgb, detected_boxes)
                                rb_after_move = self.__relocate_detected_coords(detected_boxes)

                                if not len(rb_after_move) == 1:
                                    pass
                                else:
                                    for (ex, ey, ew, eh) in rb_after_move:  # e means error.

                                        if (self.show_stream and self.augmented) or self.show_stream:
                                            self.mark_object(last_frame, ex, ey, ew, eh, 30, 50, (255, 0, 0), 2)

                                        self.target_locker.check_error(ex, ey, ew, eh)
                                break

                self.__show_frame(last_frame)
            # self.__truncate_stream()
            if self.__check_loop_ended(stop_thread):
                break

    def __detect_initiate(self, format="bgr"):
        """Method to serve as the entry point to detection, recognition and tracking features of t_system's vision ability.

        Args:
                format:       	        Color space format.
        """
        detected_boxes = []
        rgb = None

        last_frame = np.zeros(shape=(self.frame_height, self.frame_width))
        while True:
            if last_frame.any() != self.current_frame.any():
                last_frame = self.current_frame

                rgb, detected_boxes = self.detect_things(last_frame)

                if not detected_boxes:
                    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
                    if (self.show_stream and self.augmented) or self.show_stream:
                        cv2.putText(gray, "Scanning...", (int(self.frame_width - self.frame_width * 0.2), int(self.frame_height * 0.1)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 0, 0), 2)

                    self.__show_frame(gray)

                    if self.__check_loop_ended(lambda: False):
                        break
                else:
                    break
        return rgb, detected_boxes

    def scan(self, stop_thread, resolution=3):
        """Method to provide the scanning around for security mode of T_System.

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
                self.target_locker.pan.move(float(angle), 180.0)
                angle_for_ellipse_move = calc_ellipsoidal_angle(float(angle) - 90, 180.0, 75.0)  # 75 degree is for physical conditions.
                self.target_locker.tilt.move(angle_for_ellipse_move, 75.0)  # last parameter not used for both funcs
                time.sleep(0.1)

            for angle in range(180, 0, resolution * -1):
                if stop_thread():
                    break
                self.target_locker.pan.move(float(angle), 180.0)
                angle_for_ellipse_move = calc_ellipsoidal_angle(float(angle) - 90, 180.0, 75.0)
                self.target_locker.tilt.move(angle_for_ellipse_move, 75.0)  # last parameter not used for both funcs
                time.sleep(0.1)

    def reload_target_locker(self, ai=None, non_moving_target=None, arm_expansion=None):
        """The top-level method to set locking system's locker of Vision as given AI and target object status parameters.

        Args:
            ai (str):                       AI type that will using during locking the target.
            non_moving_target (bool):       Non-moving target flag.
            arm_expansion (bool):           Flag for the loading locker as expansion of the T_System's robotic arm.
        """

        self.target_locker.load_locker(ai, non_moving_target, arm_expansion)

    def serve_frame_online(self):
        """The top-level method to provide the serving video stream online for sending Flask framework based remote_ui.
        """

        is_success, im_buf_arr = cv2.imencode(".jpg", self.current_frame)
        return im_buf_arr.tobytes()  # image in byte format.

    def track_focused_point(self):
        """Method to provide the tracking predetermined non-moving target according to with locking_system's current position for track mode of T_System.

        Args:
                __stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        pass

    def __show_frame(self, frame):
        """Method to show the captured frame.

        Args:
                frame:       	        Frame matrix in bgr format.

        """

        if (self.show_stream and self.augmented) or self.show_stream:
            # show the frame
            cv2.imshow("Frame", frame)

    def __truncate_stream(self):
        """Method to clear the stream in preparation for the next frame.
        """
        self.raw_capture.seek(0)
        self.raw_capture.truncate()

    def __check_loop_ended(self, stop_thread):
        """Method to detecting FACES with hog or cnn methoda.

        Args:
                stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.

        """

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if (key == ord("q") or stop_thread()) and (self.augmented or self.active_threads):
            logger.info("All threads killed. In progress...")
            return True
        elif (key == ord("q") or stop_thread()) and not self.augmented:
            cv2.destroyAllWindows()
            self.release_members()
            return True

    def __detect_with_hog_or_cnn(self, frame):
        """Method to detecting FACES with hog or cnn methoda.

        Args:
                frame:       	        Frame matrix in bgr format.
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # rgb = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
        # r = frame.shape[1] / float(rgb.shape[1])

        detected_boxes = face_recognition.face_locations(rgb, model=self.detection_model)

        return rgb, detected_boxes

    def __detect_with_haarcascade(self, frame):
        """Method to detecting objects with haarcascade method.

        Args:
                frame:       	        Frame matrix in bgr format.
        """

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)

        detected_boxes = self.object_cascade.detectMultiScale(gray, 1.3, 5)

        # Following list's member change is for face recognition format compatibility.
        reworked_boxes = []
        for box in detected_boxes:
            # box[3] is x,
            # box[0] is y,
            # box[1] is x + w,
            # box[2] is y + h.
            reworked_boxes.append((box[1], box[0] + box[2], box[1] + box[3], box[0]))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # For __recognize_things compatibility.

        return rgb, reworked_boxes

    def __recognize_things(self, rgb, boxes):
        """Method to recognizing objects with encodings pickle files.

        Args:
                rgb:       	            Frame matrix in rgb format.
                boxes:       	        Tuple variable of locations of detected objects.
        """

        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        for encoding in encodings:

            # attempt to match each face in the input image to our known encodings
            matches = face_recognition.compare_faces(self.recognition_data["encodings"], encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face
                for i in matched_idxs:
                    name = self.recognition_data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
            names.append(name)

        return names

    def __create_tracker_by_name(self):
        """Method to creating a tracker object via type that is chosen by the user.
        """
        if self.tracker_type == self.tracker_types[0]:
            tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == self.tracker_types[1]:
            tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == self.tracker_types[2]:
            tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == self.tracker_types[3]:
            tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == self.tracker_types[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == self.tracker_types[5]:
            tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == self.tracker_types[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == self.tracker_types[7]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            logger.error('Incorrect tracker name')
            logger.info('Available trackers are:')
            for t in self.tracker_types:
                logger.info(t)

        return tracker

    @staticmethod
    def __relocate_detected_coords(detected_boxes):
        """Method to relocating members of detected boxes from given shape to wanted shape.

         Args:
                detected_boxes (tuple): Top left and bottom right coordinates of the detected thing.
        """

        reworked_boxes = []
        for box in detected_boxes:
            # box[3] is x,
            # box[0] is y,
            # box[1] is x + w,
            # box[2] is y + h.
            reworked_boxes.append((box[3], box[0], box[1] - box[3], box[2] - box[0]))

        return reworked_boxes

    def change_tracked_thing(self, file):
        """The top-level method to changing tracking objects.

         Args:
                file:       	        The haarcascade trained xml file.
        """
        ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + file + ".xml"

        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)
        self.decider.set_db(file)

    @staticmethod
    def __mark_as_single_rect(frame, x, y, w, h, radius, physically_distance, color, thickness):
        """Method to set mark_object method as drawing method with OpenCV's basic rectangle.

         Args:
                frame:       	        Frame matrix.
                x           :       	the column number of the top left point of found object from the detection method.
                y           :       	the row number of the top left point of found object from the detection method.
                w           :       	the width of found object from the detection method.
                h           :       	the height of found object from the detection method.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color (tuple):          Color of the drawing shape. In RGB Space.
                thickness (int):        Thickness of the drawing shape.
        """

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

    def __mark_as_partial_rect(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """Method to set mark_object method as drawing method with aimer's partial rect.

         Args:
                frame:       	        Frame matrix.
                x           :       	the column number of the top left point of found object from the detection method.
                y           :       	the row number of the top left point of found object from the detection method.
                w           :       	the width of found object from the detection method.
                h           :       	the height of found object from the detection method.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color (tuple):          Color of the drawing shape. In RGB Space.
                thickness (int):        Thickness of the drawing shape.
        """

        self.aimer.mark_partial_rect(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)

    def __mark_as_rotation_arcs(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """Method to set mark_object method as drawing method with aimer's rotating arcs.

         Args:
                frame:       	        Frame matrix.
                x           :       	the column number of the top left point of found object from the detection method.
                y           :       	the row number of the top left point of found object from the detection method.
                w           :       	the width of found object from the detection method.
                h           :       	the height of found object from the detection method.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color (tuple):          Color of the drawing shape. In RGB Space.
                thickness (int):        Thickness of the drawing shape.
        """

        self.aimer.mark_rotating_arcs(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)

    def __mark_as_vendor_animation(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """Method to set mark_object method as drawing method with aimer's rotating arcs.

         Args:
                frame:       	        Frame matrix.
                x           :       	the column number of the top left point of found object from the detection method.
                y           :       	the row number of the top left point of found object from the detection method.
                w           :       	the width of found object from the detection method.
                h           :       	the height of found object from the detection method.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color (tuple):          Color of the drawing shape. In RGB Space.
                thickness (int):        Thickness of the drawing shape.
        """

        self.aimer.mark_vendor_animation(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)

    def __mark_as_none(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """Method to set mark_object method for draw nothing.

         Args:
                frame:       	        Frame matrix.
                x           :       	the column number of the top left point of found object from the detection method.
                y           :       	the row number of the top left point of found object from the detection method.
                w           :       	the width of found object from the detection method.
                h           :       	the height of found object from the detection method.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color (tuple):          Color of the drawing shape. In RGB Space.
                thickness (int):        Thickness of the drawing shape.
        """
        pass

    def __get_mark_object(self, mark_found_object):
        """Method to get mark type for using when object detected.

         Args:
                mark_found_object (str):   The mark type of the detected object.
        """

        if mark_found_object == self.target_mark_types["drawings"][0]:
            return self.__mark_as_single_rect
        elif mark_found_object == self.target_mark_types["drawings"][1]:
            return self.__mark_as_partial_rect
        elif mark_found_object == self.target_mark_types["drawings"][2]:
            return self.__mark_as_rotation_arcs
        elif mark_found_object is (None or False):
            return self.__mark_as_none
        else:
            if mark_found_object in self.target_mark_types["animations"]:
                self.aimer.set_vendor_animation(mark_found_object)
                return self.__mark_as_vendor_animation

    def change_mark_object_to(self, mark_found_object):
        """Method to change mark type for using when object detected by given type.

         Args:
                mark_found_object (str):   The mark type of the detected object.
        """

        self.mark_object = self.__get_mark_object(mark_found_object)

    @staticmethod
    def __get_recognition_data(encoding_file):
        """Method to get encoded recognition data from pickle file.

         Args:
                encoding_file (str):  The file that is keep faces's encoded data.
        """

        return pickle.loads(open(encoding_file, "rb").read())  # this is recognition_data

    @dispatch(str)
    def set_recognizing(self, encoding_file):
        """The top-level method to set recognition status and parameters of Vision.

         Args:
                encoding_file (str):  The file that is keep faces's encoded data.
        """
        if not encoding_file:
            self.no_recognize = True
            self.track = self.__track_without_recognizing
            return True

        self.no_recognize = False
        self.recognition_data = self.__get_recognition_data(encoding_file)
        self.track = self.__track_with_recognizing

    @dispatch(list)
    def set_recognizing(self, encoding_files):
        """The top-level method to set recognition status and parameters of Vision.

         Args:
                encoding_files (list):  The file that is keep faces's encoded data.
        """

        self.no_recognize = False

        self.recognition_data = {"encodings": [], "names": []}

        for file in encoding_files:
            recognition_data = self.__get_recognition_data(file)
            self.recognition_data["encodings"].extend(recognition_data["encodings"])
            self.recognition_data["names"].extend(recognition_data["names"])

        self.track = self.__track_with_recognizing

    def get_current_frame(self):
        """Method to get current working camera frame.
        """
        return self.current_frame

    def __set_mqtt_receimitter(self, mqtt_receimitter):
        """Method to set mqtt_receimitter object for publishing and subscribing data echos.

         Args:
                mqtt_receimitter:          transmit and receive data function for mqtt communication
        """
        self.mqtt_receimitter = mqtt_receimitter

    def start_preview(self):
        """Method to start preview of the vision without move action.
        """
        self.camera.start_preview()

    def stop_preview(self):
        """Method to stop preview of the vision.
        """
        self.camera.stop_preview()

    def terminate_active_threads(self):
        """Method to terminate active threads of vision.
        """
        for thread in self.active_threads:
            if thread.is_alive():
                self.stop_thread = True
                thread.join()

        self.active_threads.clear()

        self.stop_thread = False

    def stop_recording(self):
        """Method to stop recording video and audio stream.
        """
        if self.record:
            self.recorder.stop()

    def __release_servos(self):
        """Method to stop sending signals to servo motors pins and clean up the gpio pins.
        """
        self.target_locker.stop()
        self.target_locker.gpio_cleanup()

    def __release_camera(self):
        """Method to stop receiving signals from the camera and stop video recording.
        """
        # self.camera.release()
        pass

    def __release_hearer(self):
        """Method to stop sending signals to servo motors pins and clean up the gpio pins.
        """
        if self.hearer:
            self.hearer.release_members()

    def release_members(self):
        """Method to close all streaming and terminate vision processes.
        """
        self.stop_recording()
        self.terminate_active_threads()
        self.__release_hearer()
        self.__release_camera()
        self.__release_servos()
