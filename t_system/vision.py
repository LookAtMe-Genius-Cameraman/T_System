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
from math import sqrt

from picamera.array import PiRGBArray

import cv2
import face_recognition
import pickle

from t_system.motor import Motor
from t_system.motor import calc_ellipsoidal_angle
from t_system.decision import Decider

from t_system.high_tech_aim import Aimer


T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

TRACKER_TYPES = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']


class Vision():
    """Class to define a vision of tracking system..

    This class provides necessary initiations and functios named :func:`t_system.vision.Vision.detect_track`
    as the loop for each camera frames for tracking mode, named :func:`t_system.vision.Vision.learn` as the
    learning ability and :func:`t_system.vision.Vision.security` as the security mode.

    """

    def __init__(self, args, camera, resolution=(320, 240), framerate=32):
        """Initialization method of :class:`t_system.vision.Vision` class.

        Args:
                camera:       	        Camera object from PiCamera.
                resolution:    	        rPi camera's resolution data.
                framerate:              rPi camera's framerate data.

        """
        # if not args["cascade_file"]:
        #     ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/frontalface_default.xml"
        #     self.decider = Decider()
        # else:

        self.detection_model = args["detection_model"]

        if self.detection_model == "haarcascade":
            self.detect_things = self.detect_with_haarcascade
        else:
            self.detect_things = self.detect_with_hog_or_cnn

        if args['use_tracking_api']:
            self.track = self.track_with_cv_tracking_api
        else:
            self.track = self.track_without_cv_tracking_api

        encoding_pickle_file = T_SYSTEM_PATH + "/recognition_encodings/" + args["encoding_file"] + ".pickle"
        self.recognition_data = pickle.loads(open(encoding_pickle_file, "rb").read())

        # Specify the tracker type
        self.tracker_type = args["tracker_type"]

        self.camera = camera
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        # self.camera.start_preview()

        self.rawCapture = PiRGBArray(camera, size=resolution)

        ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + args["cascade_file"] + ".xml"
        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)

        (self.frame_width, self.frame_height) = resolution

        self.decider = Decider(args["cascade_file"])

        self.servo_pan = Motor(args["gpio_pan_tilt"][0], self.decider)                # pan means rotate right and left ways.
        self.servo_tilt = Motor(args["gpio_pan_tilt"][1], self.decider, 4.5, False)   # tilt means rotate up and down ways.

        self.aimer = Aimer()

        self.show_stream = args["show_stream"]  # 'show-stream' argument automatically converted this type.
        self.augmented = args["augmented"]

        self.mqtt_receimitter = None

        # Allow the camera to warm up
        time.sleep(0.1)

    def detect_track(self, stop_thread, format="bgr"):
        """The top-level method to real time object detection.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        self.track(stop_thread, format)

        cv2.destroyAllWindows()
        self.camera.release()

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

            rgb, detected_boxes = self.detect_things(frame)

            # names = self.recognize_things(rgb, detected_boxes)

            reworked_boxes = []
            for box in detected_boxes:
                # box[3] is x,
                # box[0] is y,
                # box[1] is x + w,
                # box[2] is y + h.
                reworked_boxes.append((box[3], box[0], box[1] - box[3], box[2] - box[0]))

            if not len(reworked_boxes) == 1:
                pass
            else:
                for (x, y, w, h) in reworked_boxes:

                    if (self.show_stream and self.augmented) or self.show_stream:
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

                            if (self.show_stream and self.augmented) or self.show_stream:
                                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                            err_rate_pan = float(self.servo_pan.current_dis_to_des(x, x+w, self.frame_width) / self.servo_pan.get_previous_dis_to_des()) * 100
                            err_rate_tilt = float(self.servo_tilt.current_dis_to_des(y, y+h, self.frame_height) / self.servo_tilt.get_previous_dis_to_des()) * 100

                            self.decider.decision(obj_width_pan, err_rate_pan, True)
                            self.decider.decision(obj_width_tilt, err_rate_tilt, True)

            if (self.show_stream and self.augmented) or self.show_stream:
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
        """The low-level method to provide the scanning around for security mode of T_System.

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
        """The low-level method to provide the video stream for security mode of T_System.

        Args:
                stop_thread:   	       Stop flag of the tread about terminating it outside of the function's loop.
                resolution:            angle's step width between 0 - 180 degree.
        """
        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # gray = cv2.equalizeHist(gray)

            # SECURITY MODE CAN BE TAKING PHOTOGRAPHS AS DIFFERENT FROM learn AND detect_track FUNCTIONS.
            # objects = self.object_cascade.detectMultiScale(gray, 1.3, 5)
            #
            # if not len(objects) == 1:
            #     pass
            # else:
            #     for (x, y, w, h) in objects:
            #         if (self.show_stream and self.augmented) or self.show_stream:
            #             cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if (self.show_stream and self.augmented) or self.show_stream:
                # show the frame
                cv2.imshow("Frame", image)

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                break

        # if loop end, the scan process will be terminated.

    def create_tracker_by_name(self):
        """The low-level method to creating a tracker object via type that is chosen by the user.
        """
        if self.tracker_type == TRACKER_TYPES[0]:
            tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == TRACKER_TYPES[1]:
            tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == TRACKER_TYPES[2]:
            tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == TRACKER_TYPES[3]:
            tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == TRACKER_TYPES[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == TRACKER_TYPES[5]:
            tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == TRACKER_TYPES[6]:
            tracker = cv2.TrackerMOSSE_create()
        elif self.tracker_type == TRACKER_TYPES[7]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            print('Incorrect tracker name')
            print('Available trackers are:')
            for t in TRACKER_TYPES:
                print(t)

        return tracker

    def detect_with_hog_or_cnn(self, frame):
        """The low-level method to detecting FACES with hog or cnn methoda.

        Args:
                frame:       	        Frame matrix in bgr format.
        """

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # rgb = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
        # r = frame.shape[1] / float(rgb.shape[1])

        detected_boxes = face_recognition.face_locations(rgb, model=self.detection_model)

        return rgb, detected_boxes

    def detect_with_haarcascade(self, frame):
        """The low-level method to detecting objects with haarcascade method.

        Args:
                frame:       	        Frame matrix in bgr format.
        """

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        detected_boxes = self.object_cascade.detectMultiScale(gray, 1.3, 5)

        # Following list's member change is for face recognition format compatibility.
        reworked_boxes = []
        for box in detected_boxes:
            # box[3] is x,
            # box[0] is y,
            # box[1] is x + w,
            # box[2] is y + h.
            reworked_boxes.append((box[1], box[0] + box[2], box[1] + box[3], box[0]))

        return rgb, reworked_boxes

    def recognize_things(self, rgb, boxes):
        """The low-level method to recognizing objects with encodings pickle files.

        Args:
                rgb:       	            Frame matrix in rgb format.
                boxes:       	        Tuple variable of locations of detected objects.
        """

        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
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
                # each recognized face face
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

    def track_without_cv_tracking_api(self, stop_thread, format='bgr'):
        """The low-level method to provide detecting and tracking objects without using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
            frame = frame.array
            frame = frame.copy()  # For reaching with overwrite privileges.

            rgb, detected_boxes = self.detect_things(frame)

            names = self.recognize_things(rgb, detected_boxes)

            reworked_boxes = []
            for box in detected_boxes:
                # box[3] is x,
                # box[0] is y,
                # box[1] is x + w,
                # box[2] is y + h.
                reworked_boxes.append((box[3], box[0], box[1] - box[3], box[2] - box[0]))

            for (x, y, w, h), name in zip(reworked_boxes, names):

                physically_distance = self.servo_pan.get_physically_distance(w)  # for calculating the just about physically distance of object.
                radius = int(sqrt(w * w + h * h) / 2)

                if name == "Unknown":
                    if (self.show_stream and self.augmented) or self.show_stream:
                        frame = self.aimer.mark_rotating_arcs(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)
                else:
                    self.servo_pan.move(x, x + w, self.frame_width)
                    self.servo_tilt.move(y, y + h, self.frame_height)

                    if (self.show_stream and self.augmented) or self.show_stream:
                        frame = self.aimer.mark_parital_rect(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)

                        # NAME AND FOUNDED KNOWLEDGES WILL PASS TO AIMER. AND CONFLICT ON LEARNING OF TRACKING DATABASE NAMES WILL RESOLVE.

            time.sleep(0.1)  # Allow the servos to complete the moving.

            if (self.show_stream and self.augmented) or self.show_stream:
                # show the frame
                cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                break

    def track_with_cv_tracking_api(self, stop_thread, format='bgr'):
        """The low-level method to provide detecting and tracking objects with using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        tracked_boxes = []  # this became array.  because of overriding.
        names = []

        multi_tracker = cv2.MultiTracker_create()

        rgb, detected_boxes = self.initiate()

        found_count = 0
        d_t_failure_count = 0
        use_detection = 0

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            if len(detected_boxes) > len(tracked_boxes):
                names = self.recognize_things(rgb, detected_boxes)

                frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

                # Create MultiTracker object
                multi_tracker = cv2.MultiTracker_create()

                # Initialize MultiTracker
                for box in detected_boxes:
                    # box[3] is x,
                    # box[0] is y,
                    # box[1] is x + w,
                    # box[2] is y + h.
                    reworked_box = box[3], box[0], box[1] - box[3], box[2] - box[0]

                    multi_tracker.add(self.create_tracker_by_name(), frame, reworked_box)
                found_count += 1

            # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
            frame = frame.array
            frame = frame.copy()  # For reaching with overwrite privileges.

            if use_detection >= 3:
                rgb, detected_boxes = self.detect_things(frame)
                use_detection = 0

            use_detection += 1

            # Start timer
            timer = cv2.getTickCount()

            # get updated location of objects in subsequent frames
            is_tracking_success, tracked_boxes = multi_tracker.update(frame)

            if not len(detected_boxes) >= len(tracked_boxes):
                d_t_failure_count += 1
            else:
                d_t_failure_count = 0

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            if is_tracking_success and d_t_failure_count < 5:

                for (x, y, w, h), name in zip(tracked_boxes, names):

                    physically_distance = self.servo_pan.get_physically_distance(w)  # for calculating the just about physically distance of object.
                    radius = int(sqrt(w * w + h * h) / 2)

                    if name == "Unknown":
                        if (self.show_stream and self.augmented) or self.show_stream:
                            frame = self.aimer.mark_rotating_arcs(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)
                    else:
                        self.servo_pan.move(x, x + w, self.frame_width)
                        self.servo_tilt.move(y, y + h, self.frame_height)

                        if (self.show_stream and self.augmented) or self.show_stream:
                            frame = self.aimer.mark_parital_rect(frame, (int(x + w / 2), int(y + h / 2)), radius, physically_distance)

                            # NAME AND FOUNDED KNOWLEDGES WILL PASS TO AIMER. AND CONFLICT ON LEARNING OF TRACKING DATABASE NAMES WILL RESOLVE.

                time.sleep(0.1)  # Allow the servos to complete the moving.

            elif not is_tracking_success or d_t_failure_count >= 5:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                tracked_boxes = []  # for clearing tracked_boxes list.

            # # Display tracker type on frame
            # cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            #
            # # Display FPS on frame
            # cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            if (self.show_stream and self.augmented) or self.show_stream:
                # show the frame
                cv2.imshow("Frame", frame)

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            key = cv2.waitKey(1) & 0xFF
            # if the `q` key was pressed, break from the loop
            if key == ord("q") or stop_thread():
                # print("thread killed")
                break

    def initiate(self, format="bgr"):
        """The low-level method to serve as the entry point to detection, recognition and tracking features of t_system's vision ability.

        Args:
                format:       	        Color space format.
        """
        detected_boxes = []
        rgb = None

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            frame = frame.array
            frame = frame.copy()  # For reaching with overwrite privileges.

            rgb, detected_boxes = self.detect_things(frame)

            if not detected_boxes:
                gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

                cv2.putText(gray, "Scanning...", (self.frame_width - self.frame_width * 0.1, self.frame_height * 0.1), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 0, 0), 2)

                # show frame
                cv2.imshow('MultiTracker', gray)

                # quit on ESC button
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Q pressed
                    cv2.destroyAllWindows()
                    self.camera.release()
                    break
            else:
                break

        return rgb, detected_boxes

    def change_tracked_thing(self, file):
        """The top-level method to changing tracking objects.

         Args:
                file:       	        The haarcascade trained xml file.
        """
        ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + file + ".xml"

        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)
        self.decider.set_db(file)

    def set_mqtt_receimitter(self, mqtt_receimitter):
        """The top-level method to set mqtt_receimitter object for publishing and subscribing data echos.

         Args:
                mqtt_receimitter:          transmit and receive data function for mqtt communication
        """
        self.mqtt_receimitter = mqtt_receimitter
