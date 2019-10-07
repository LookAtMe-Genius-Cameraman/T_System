#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: job
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's vision.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import threading

from t_system.administration import is_admin
from t_system import seer
from t_system import arm
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

        self.stop_mission = False
        self.pause_mission = False
        self.mission_thread = threading.Thread(target=mission_manager.execute, args=(lambda: self.stop_mission, lambda: self.pause_mission, "initial", "scenario",  self.predicted_mission))

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

    def start_job(self, admin_id, running_type):
        """The top-level method to start seer's work.

        Args:
            admin_id (str):                 Root privileges flag.
            running_type (str):             Specifier of running type. Either `simulation` or `real`.
        """
        result = True

        if running_type == "simulation":
            seer.record = False
        elif running_type == "real":
            seer.record = True
        else:
            result = False

        self.mission_thread = threading.Thread(target=mission_manager.continuous_execute, args=(lambda: self.stop_mission, lambda: self.pause_mission, self.scenario, "scenario",  self.predicted_mission))
        self.mission_thread.start()

        seer.watch_and(self.job_type)

        return result

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

    def stop_job(self, admin_id):
        """Method to stop the work of seer.

        Args:
            admin_id (str):                 Root privileges flag.
        """

        seer.terminate_active_threads()

        record_manager.refresh_records()

        self.__stop_mission_thread()

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

    @staticmethod
    def __set_track_approach(ai, non_moving_target):
        """Method to set mission scenarios of the job.

        Args:
            ai (str):                       AI type that will using during job.
            non_moving_target (bool):       Non-moving target flag.
        """

        if ai:
            mission_manager.revert_the_expand_actor()

        seer.reload_target_locker(ai, non_moving_target)

        if non_moving_target:
            mission_manager.expand_actor()

    def __stop_mission_thread(self):
        """Method to stop the mission_thread.
        """

        if self.mission_thread.is_alive():
            self.stop_mission = True
            self.mission_thread.join()
            self.stop_mission = False
