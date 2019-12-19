#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: job
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's vision.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import multiprocessing
import threading
import time  # Time access and conversions

from t_system import seer
from t_system import mission_manager

from t_system import record_manager
from t_system import face_encode_manager
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class JobManager:
    """Class to define a manager for asynchronous work of t_system's vision ability.

        This class provides necessary initiations and a function named
        :func:`t_system.motion.LockingSystem.NonMovingTargetLocker.lock`
        for the provide move of servo motor during locking to the target.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.modules.vision.VisionManager` class.
        """

        self.job_type = ""
        self.scenario = ""
        self.predicted_mission = False
        self.non_moving_target = False

        self.stop_mission = False
        self.pause_mission = False
        self.mission_proc = multiprocessing.Process(target=mission_manager.execute, args=(lambda: self.stop_mission, lambda: self.pause_mission, "initial", "scenario", self.predicted_mission))

        self.stop_watch = False
        self.watch_thread = threading.Thread(target=seer.watch, args=(lambda: self.stop_mission, "bgr", self.job_type))

    def set_seer(self, admin_id, data):
        """The top-level method to set seer's work parameters.

        Args:
                admin_id (str):                 Root privileges flag.
                data (dict):                    Job data structure.
        """

        self.job_type = data["job_type"]
        self.scenario = data["scenario"]
        self.predicted_mission = data["predicted_mission"]

        self.__set_recognition(data["recognized_persons"])
        self.__set_track_approach(data["ai"], data["non_moving_target"])

        return True

    @staticmethod
    def change_found_object_mark(admin_id, mark):
        """The top-level method to change mark type of found object.

        Args:
                admin_id (str):                 Root privileges flag.
                mark (str):                    The mark type of the detected object.
        """
        if mark in ["false", "False"]:
            mark = False

        seer.change_mark_object_to(mark)

    @staticmethod
    def get_found_object_marks(admin_id):
        """The top-level method to change mark type of found object.

        Args:
                admin_id (str):                 Root privileges flag.
        """

        return seer.target_mark_types

    def execute_job(self, admin_id, cause):
        """The top-level method to start seer's work.

        Args:
                admin_id (str):                 Root privileges flag.
                cause (str):                    Specifier of running type. Either `take_shots`, `track`, `record` or `mission`.
        """
        if cause == "take_shots":
            seer.take_shots()
            time.sleep(0.3)
            record_manager.refresh_records(r_type="shot")
            return True
        elif cause == "track":
            self.__start_track()
        elif cause == "record":
            self.__start_record()
        elif cause == "mission":
            self.__start_mission()
        elif cause == "live_stream":
            self.__start_live_stream()
        else:
            return False
        return True

    def resume_job(self, admin_id):
        """Method to resume the paused work of seer.

        Args:
                admin_id (str):                 Root privileges flag.
        """

        return True

    def pause_job(self, admin_id):
        """Method to pause the work of seer.

        Args:
                admin_id (str):                 Root privileges flag.
        """

        return True

    def stop_job(self, admin_id, cause):
        """Method to stop the work of seer.

        Args:
                admin_id (str):                 Root privileges flag.
                cause (str):                 Specifier of running type. Either `simulation` or `real`.
        """

        if cause == "track":
            self.__stop_track()
        elif cause == "record":
            self.__stop_record()
        elif cause == "mission":
            self.__stop_mission_proc()
        elif cause == "live_stream":
            self.__stop_live_stream()
        else:
            return False
        return True

    @staticmethod
    def __set_recognition(recognized_persons):
        """Method to set seer's recognition status.

        Args:
                recognized_persons (list):        The name it's owner will recognized by seer.
        """

        if not recognized_persons:
            seer.set_recognizing("")
        elif recognized_persons[0] == "all":
            seer.set_recognizing(face_encode_manager.main_encoding_file)
        else:
            faces = face_encode_manager.get_faces(recognized_persons)
            seer.set_recognizing([face.pickle_file for face in faces])

    def __set_track_approach(self, ai, non_moving_target):
        """Method to set mission scenarios of the job.

        Args:
                ai (str):                       AI type that will using during job.
                non_moving_target (bool):       Non-moving target flag.
        """
        self.non_moving_target = non_moving_target

        if ai:
            mission_manager.revert_the_expand_actor()

        seer.reload_target_locker(ai, non_moving_target)

        if non_moving_target:
            mission_manager.expand_actor()

    def __start_track(self):
        """The top-level method to start seer's tracking work.
        """
        if not self.non_moving_target:
            rgb, detected_boxes = seer.detect_initiate(lambda: self.stop_watch)

            if detected_boxes:
                seer.watch_and(self.job_type)

            time.sleep(0.5)

        else:
            self.watch_thread = threading.Thread(target=seer.watch, args=(lambda: self.stop_watch, "bgr", self.job_type))
            self.watch_thread.start()

    def __stop_track(self):
        """The top-level method to stop seer's tracking work.
        """

        seer.terminate_active_threads()
        seer.stop_thread = True

        self.__stop_watch_thread()

        time.sleep(0.15)
        seer.stop_thread = False

    def __start_record(self):
        """The top-level method to start seer's recording work.
        """
        self.__stop_track()
        seer.record = True

        seer.watch_and(self.job_type)

    def __stop_record(self):
        """The top-level method to stop seer's recording work.
        """

        self.__stop_track()

        record_manager.refresh_records()
        seer.record = False

        seer.watch_and(self.job_type)

    def __start_live_stream(self):
        """The top-level method to start seer's live-streaming work.
        """

        seer.online_streamer.go_live()

    def __stop_live_stream(self):
        """The top-level method to stop seer's live-streaming work.
        """

        seer.online_streamer.stop_live()

    def __start_mission(self):
        """The top-level method to start T_System's MissionManager mission.
        """

        self.mission_proc = multiprocessing.Process(target=mission_manager.continuous_execute, args=(lambda: self.stop_mission, lambda: self.pause_mission, self.scenario, "scenario", self.predicted_mission))
        self.mission_proc.start()

    def __stop_mission_proc(self):
        """Method to stop the mission_thread.
        """

        if self.mission_proc.is_alive():
            self.stop_mission = True
            self.mission_proc.terminate()
            self.stop_mission = False
    
    def __stop_watch_thread(self):
        """Method to stop the watch_thread.
        """

        if self.watch_thread.is_alive():
            self.stop_watch = True
            self.watch_thread.join()
            self.stop_watch = False
