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
from picamera import PiCamera
from picamera.array import PiRGBArray

import cv2
import face_recognition
import pickle

from t_system.motion.arm import Arm
from t_system.motion.locking_system import LockingSystem
from t_system.motion import calc_ellipsoidal_angle
from t_system.decision import Decider
from t_system.audition import Hearer
from t_system.recordation import Recorder

from t_system.high_tech_aim import Aimer


T_SYSTEM_PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

TRACKER_TYPES = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']


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

        self.detection_model = args["detection_model"]

        if self.detection_model == "haarcascade":
            self.detect_things = self.detect_with_haarcascade
        else:
            self.detect_things = self.detect_with_hog_or_cnn

        if args['use_tracking_api']:
            self.detect_track = self.d_t_with_cv_ta
        else:
            self.detect_track = self.d_t_without_cv_ta

        self.no_recognize = args["no_recognize"]

        if not self.no_recognize:
            encoding_pickle_file = T_SYSTEM_PATH + "/recognition_encodings/" + args["encoding_file"] + ".pickle"
            self.recognition_data = pickle.loads(open(encoding_pickle_file, "rb").read())

            self.track = self.track_with_recognizing
        else:
            self.track = self.track_without_recognizing

        # Specify the tracker type
        self.tracker_type = args["tracker_type"]

        self.hearer = Hearer(args)

        resolution = (args["resolution"][0], args["resolution"][0])
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = args["framerate"]
        # self.camera.start_preview()
        
        self.recorder = Recorder(self.camera, self.hearer)

        self.rawCapture = PiRGBArray(self.camera, size=resolution)

        ccade_xml_file = T_SYSTEM_PATH + "/haarcascade/" + args["cascade_file"] + ".xml"
        self.object_cascade = cv2.CascadeClassifier(ccade_xml_file)

        (self.frame_width, self.frame_height) = resolution

        self.decider = None
        if args["AI"] == "official_ai":
            self.decider = Decider(args["cascade_file"])

        self.target_locker = LockingSystem(args, resolution, self.decider)

        self.arm = None
        if args["robotic_arm"]:
            self.arm = Arm(args["robotic_arm"])

        self.aimer = Aimer()

        self.show_stream = args["show_stream"]  # 'show-stream' argument automatically converted this type.
        self.mark_object = self.get_mark_object(args["found_object_mark"])

        self.record = args["record"]
        self.record_path = ""
        self.record_name = ""

        self.augmented = False
        if args["interface"] == "augmented":
            self.augmented = True

        self.mqtt_receimitter = None

        # Allow the camera to warm up
        time.sleep(0.1)

    def d_t_without_cv_ta(self, stop_thread, format='bgr'):
        """The low-level method to provide detecting and tracking objects without using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        if self.record:
            self.recorder.start("track")

        self.detect_initiate()

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            # grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
            frame = frame.array
            frame = frame.copy()  # For reaching with overwrite privileges.

            rgb, detected_boxes = self.detect_things(frame)
            reworked_boxes = self.relocate_detected_coords(detected_boxes)

            if not self.no_recognize:
                names = self.recognize_things(rgb, detected_boxes)
            else:
                names = None

            self.track(frame, reworked_boxes, names)

            # time.sleep(0.1)  # Allow the servos to complete the moving.

            self.show_frame(frame)
            self.truncate_stream()
            # print("frame showed!")
            if self.check_loop_ended(stop_thread):
                break

    def d_t_with_cv_ta(self, stop_thread, format='bgr'):
        """The low-level method to provide detecting and tracking objects with using OpenCV's tracking API.

        Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        if self.record:
            self.recorder.start("track")

        tracked_boxes = []  # this became array.  because of overriding.
        names = []

        multi_tracker = cv2.MultiTracker_create()

        rgb, detected_boxes = self.detect_initiate()

        found_count = 0
        d_t_failure_count = 0
        use_detection = 0

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            if len(detected_boxes) > len(tracked_boxes):

                if not self.no_recognize:
                    names = self.recognize_things(rgb, detected_boxes)
                else:
                    names = None

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

                self.track(frame, tracked_boxes, names)

            elif not is_tracking_success or d_t_failure_count >= 5:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                tracked_boxes = []  # for clearing tracked_boxes list.

            # # Display tracker type on frame
            # cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
            #
            # # Display FPS on frame
            # cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            self.show_frame(frame)
            self.truncate_stream()

            if self.check_loop_ended(stop_thread):
                break

    def track_without_recognizing(self, frame, boxes, names):
        """The low-level method to track the objects without recognize them, for detect_track methods.

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

            # time.sleep(0.1)  # Allow the servos to complete the moving.

    def track_with_recognizing(self, frame, boxes, names):
        """The low-level method to track the objects with recognize them, for detect_track methods.

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

        # time.sleep(0.1)  # Allow the servos to complete the moving.

    def learn(self, stop_thread, format="bgr"):
        """The top-level method to learn how to track objects.

         Args:
                stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        if self.record:
            self.recorder.start("learn")

        self.detect_initiate()

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text

            image = frame.array
            image = image.copy()  # For reaching with overwrite privileges.
            # err_check_image = None

            rgb, detected_boxes = self.detect_things(image)
            # names = self.recognize_things(rgb, detected_boxes)
            reworked_boxes = self.relocate_detected_coords(detected_boxes)

            if not len(reworked_boxes) == 1:
                # self.show_frame(image)
                pass
            else:
                for (x, y, w, h) in reworked_boxes:

                    if (self.show_stream and self.augmented) or self.show_stream:
                        self.mark_object(image, x, y, w, h, 30, 50, (255, 0, 0), 2)
                    obj_width = w
                    # obj_area = w * h  # unit of obj_width is px ^ 2.

                    self.target_locker.lock(x, y, w, h)

                    # time.sleep(0.2)  # allow the camera to capture after moving.

                    # self.show_frame(image)
                    self.truncate_stream()

                    self.camera.capture(self.rawCapture, format=format)
                    err_check_image = self.rawCapture.array

                    rgb, detected_boxes = self.detect_things(err_check_image)
                    # names = self.recognize_things(rgb, detected_boxes)
                    rb_after_move = self.relocate_detected_coords(detected_boxes)

                    if not len(rb_after_move) == 1:
                        # self.show_frame(err_check_image)
                        pass
                    else:
                        for (ex, ey, ew, eh) in rb_after_move:  # e means error.

                            if (self.show_stream and self.augmented) or self.show_stream:
                                self.mark_object(image, ex, ey, ew, eh, 30, 50, (255, 0, 0), 2)

                            self.target_locker.check_error(ex, ey, ew, eh)

                            # self.show_frame(image)

            self.show_frame(image)
            self.truncate_stream()
            if self.check_loop_ended(stop_thread):
                break

    def detect_initiate(self, format="bgr"):
        """The low-level method to serve as the entry point to detection, recognition and tracking features of t_system's vision ability.

        Args:
                format:       	        Color space format.
        """
        detected_boxes = []
        rgb = None

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):

            frame = frame.array
            frame = frame.copy()  # For reaching to frame with overwrite privileges.

            rgb, detected_boxes = self.detect_things(frame)

            if not detected_boxes:
                gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
                if (self.show_stream and self.augmented) or self.show_stream:
                    cv2.putText(gray, "Scanning...", (int(self.frame_width - self.frame_width * 0.2), int(self.frame_height * 0.1)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (200, 0, 0), 2)

                self.show_frame(gray)
                self.truncate_stream()

                if self.check_loop_ended(lambda: False):
                    break
            else:
                self.rawCapture.truncate(0)
                break
        return rgb, detected_boxes

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

    def stream(self, stop_thread, format="bgr"):
        """The low-level method to provide the video stream for security mode of T_System.

        Args:
                stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """

        if self.record:
            self.recorder.start("security")

        for frame in self.camera.capture_continuous(self.rawCapture, format=format, use_video_port=True):
            # inside of the loop is optionally editable.
            image = frame.array

            self.show_frame(image)
            self.truncate_stream()

            if self.check_loop_ended(stop_thread):
                break

    def track_focused_point(self):
        """The high-level method to provide the tracking predetermined non-moving target according to with locking_system's current position for track mode of T_System.

        Args:
                stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.
                format:       	        Color space format.
        """
        pass

    def show_frame(self, frame):
        """The low-level method to show the captured frame.

        Args:
                frame:       	        Frame matrix in bgr format.

        """

        if (self.show_stream and self.augmented) or self.show_stream:
            # show the frame
            cv2.imshow("Frame", frame)

    def truncate_stream(self, ):
        """The low-level method to clear the stream in preparation for the next frame.
        """
        self.rawCapture.truncate(0)

    def check_loop_ended(self, stop_thread):
        """The low-level method to detecting FACES with hog or cnn methoda.

        Args:
                stop_thread:   	        Stop flag of the tread about terminating it outside of the function's loop.

        """

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if (key == ord("q") or stop_thread()) and self.augmented:
            # print("thread killed")
            return True
        elif (key == ord("q") or stop_thread()) and not self.augmented:
            cv2.destroyAllWindows()
            self.release_camera()
            self.release_servos()
            self.release_hearer()
            return True

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

        detected_boxes = self.object_cascade.detectMultiScale(gray, 1.3, 5)

        # Following list's member change is for face recognition format compatibility.
        reworked_boxes = []
        for box in detected_boxes:
            # box[3] is x,
            # box[0] is y,
            # box[1] is x + w,
            # box[2] is y + h.
            reworked_boxes.append((box[1], box[0] + box[2], box[1] + box[3], box[0]))

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # For recognize_things compatibility.

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

    @staticmethod
    def relocate_detected_coords(detected_boxes):
        """The low-level method to relocating members of detected boxes from given shape to wanted shape.

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

    def mark_as_single_rect(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """The low-level method to set mark_object method as drawing method with OpenCV's basic rectangle.

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

    def mark_as_partial_rect(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """The low-level method to set mark_object method as drawing method with aimer's partial rect.

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

    def mark_as_rotation_arcs(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """The low-level method to set mark_object method as drawing method with aimer's rotating arcs.

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

    def mark_as_none(self, frame, x, y, w, h, radius, physically_distance, color, thickness):
        """The low-level method to set mark_object method for draw nothing.

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

    def get_mark_object(self, mark_found_object):
        """The low-level method to set mqtt_receimitter object for publishing and subscribing data echos.

         Args:
                mark_found_object (str):   The mark type of the detected object.
        """

        if mark_found_object == "single_rect":
            return self.mark_as_single_rect
        elif mark_found_object == "partial_rect":
            return self.mark_as_partial_rect
        elif mark_found_object == "rotating_arcs":
            return self.mark_as_rotation_arcs
        else:
            return self.mark_as_none

    def set_mqtt_receimitter(self, mqtt_receimitter):
        """The low-level method to set mqtt_receimitter object for publishing and subscribing data echos.

         Args:
                mqtt_receimitter:          transmit and receive data function for mqtt communication
        """
        self.mqtt_receimitter = mqtt_receimitter

    def release_servos(self):
        """The low-level method to stop sending signals to servo motors pins and clean up the gpio pins.
        """

        self.target_locker.stop()
        self.target_locker.gpio_cleanup()

    def release_camera(self):
        """The low-level method to stop receiving signals from the camera and stop video recording.
        """

        # self.camera.release()
        if self.record:
            self.camera.stop_recording()

    def release_hearer(self):
        """The low-level method to stop sending signals to servo motors pins and clean up the gpio pins.
        """

        self.hearer.release_members()
