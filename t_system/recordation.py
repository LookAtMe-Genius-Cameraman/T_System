#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: recordation
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's recording video and audio ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import os  # Miscellaneous operating system interfaces
import datetime  # Basic date and time types
import subprocess  # Subprocess managements
import uuid  # The random id generator

from shutil import rmtree
from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher

from t_system import dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class Recorder:
    """Class to define a recording ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.recordation.RecordManager.start`
    for creating a Record object and start recording by this object. :func:`t_system.recordation.RecordManager.merge_audio_and_video`
    for merging separate audio and video file to one.
    """

    def __init__(self, shot_format, shoot_formats, camera, hearer):
        """Initialization method of :class:`t_system.recordation.Recorder` class.

        Args:
                shot_format (str):      Format of the shot. (jpg, png etc.)
                shoot_formats (list):   Formats of the records for video, audio and merged.
                camera:       	        Camera object from PiCamera.
                hearer:       	        Hearer object.
        """

        self.current_shoot_params = {"video_file": "", "audio_file": "", "merged_file": ""}
        self.current_shot_params = {"file": ""}

        self.current_video_file = ""
        self.current_audio_file = ""
        self.current_merged_file = ""

        self.shoot_formats = {"video": shoot_formats[0], "audio": shoot_formats[1], "merged": shoot_formats[2]}
        self.shot_format = shot_format

        self.camera = camera
        self.hearer = hearer

    def take_shots(self):
        """Method to take shots.
        """
        shot = Shot(datetime.datetime.now().strftime("%d_%m_%Y"), datetime.datetime.now().strftime("%H_%M_%S"), self.shot_format)

        self.__set_record_params("shot", shot)

        self.camera.capture(self.current_shot_params["file"])

    def start_shoot(self, mode="track"):
        """Method to start audio and video recording asynchronously.

         Args:
                mode:       	        The running mode which is wants to set video name.
        """
        logger.debug("Record starting...")
        record = Shoot(datetime.datetime.now().strftime("%d_%m_%Y"), datetime.datetime.now().strftime("%H_%M_%S"), mode, self.shoot_formats)

        self.__set_record_params("shoot", record)

        self.camera.start_recording(self.current_shoot_params["video_file"], self.shoot_formats["video"])
        self.hearer.start_recording(self.current_shoot_params["audio_file"], self.shoot_formats["audio"])

    def stop_shoot(self):
        """Method to stop audio and video recording
        """

        if self.camera.recording:
            self.camera.stop_recording()
        self.hearer.stop_recording()

        # Todo: This is disgusting way to merging audio and silent video. Fix this.
        self.merge_audio_and_video()

    def merge_audio_and_video(self):
        """Method to merge recorded audio and video files.
        """

        merge_cmd = f'ffmpeg -y -i {self.current_shoot_params["audio_file"]} -r 24 -i {self.current_shoot_params["video_file"]} -filter:a aresample=async=1 -c:a flac -strict -2 -c:v copy {self.current_shoot_params["merged_file"]}'

        subprocess.call(merge_cmd, shell=True)

        logger.info('Video and Audio Muxing Done')

    def __set_record_params(self, r_type, record):
        """Method to setting current parameter by current recording.

        Args:
                r_type (str):  record type. "shoot" or "shot".
                record:        Shot or Record instance.
        """

        if r_type == "shoot":
            self.current_shoot_params["video_file"] = record.video_file
            self.current_shoot_params["audio_file"] = record.audio_file
            self.current_shoot_params["merged_file"] = record.merged_file
        elif r_type == "shot":
            self.current_shot_params["file"] = record.shot_file


class RecordManager:
    """Class to define Record manager for handling the recordation database of t_system's vision.

    This class provides necessary initiations and functions named :func:`t_system.recordation.RecordManager.get_records`
    for returning the Record objects of existing records with given table(date at the same time) parameter.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.recordation.RecordManager` class.
        """

        self.records_folder = f'{dot_t_system_dir}/records'

        self.__check_folders()

        self.shoots_table = DBFetcher(self.records_folder, "db", "shoots").fetch()
        self.shot_table = DBFetcher(self.records_folder, "db", "shots").fetch()

        self.shoots = []
        self.shots = []

        self.__set_records()
        
    def __set_records(self, r_type=None):
        """Method to set existing members by given members type If the members parameter is None it set's all members.
        
        Args:
                r_type (str):  record type. "shoot" or "shot".
        """
        
        if r_type == "shoot":
            for record in self.shoots_table.all():
                self.shoots.append(Shoot(record["date"], record["time"], record["scope"], record["record_formats"], record["id"], record["name"], record["length"]))
        elif r_type == "shot":
            for shot in self.shot_table.all():
                self.shots.append(Shot(shot["date"], shot["time"], shot["shot_format"], shot["id"], shot["name"], shot["size"]))
        
        elif r_type is None:
            for record in self.shoots_table.all():
                self.shoots.append(Shoot(record["date"], record["time"], record["scope"], record["record_formats"], record["id"], record["name"], record["length"]))
            for shot in self.shot_table.all():
                self.shots.append(Shot(shot["date"], shot["time"], shot["shot_format"], shot["id"], shot["name"], shot["size"]))

    def refresh_records(self, r_type=None):
        """Method to refresh_records existing members by given members parameter on runtime alterations.
        
        Args:
                r_type (str):  record type. "record" or "shot".
        """
        if r_type in ["shoot", "shot"]:
            if r_type == "shoot":
                self.shoots.clear()

            elif r_type == "shot":
                self.shots.clear()

            elif r_type is None:
                self.shoots.clear()
                self.shots.clear()
        
            self.__set_records(r_type=r_type)

    def get_records(self, r_type=None, date=None):
        """Method to get existing records in given date. If date is None it returns all records.

         Args:
                r_type (str):   record type. "shoot" or "shot".
                date (str):     Parent date of the record. In day_mount_year format.
        """
        records = []

        if r_type == "shoot":
            records.extend(self.shoots)
        elif r_type == "shot":
            records.extend(self.shots)
        elif r_type is None:
            records.extend(self.shoots)
            records.extend(self.shots)

        _records = []

        if date:
            for record in records:
                if record.date == date:
                    _records.append(record)
            return _records

        return records

    def get_record(self, r_id):
        """Method to get existing records in given id and type.

         Args:
                r_id (str):     ID of the record.
        """

        for shoot in self.shoots:
            if shoot.id == r_id:
                return shoot, "shoot"

        for shot in self.shots:
            if shot.id == r_id:
                return shot, "shot"

        return None, None

    def get_record_dates(self, r_type=None):
        """Method to get date list of existing records.

         Args:
                r_type (str):   record type. "shoot" or "shot".
        """
        records = []

        if r_type == "shoot":
            records.extend(self.shoots)
        elif r_type == "shot":
            records.extend(self.shots)
        elif r_type is None:
            records.extend(self.shoots)
            records.extend(self.shots)

        dates = []
        for record in records:
            dates.append(record.date)

        dates = list(dict.fromkeys(dates))  # removes duplicated dates.

        return dates

    def delete_record(self, r_id):
        """Method to get date list of existing records.

         Args:
                r_id (str):               ID of the record.
        """

        for shoot in self.shoots:
            if shoot.id == r_id:
                shoot.remove_self()
                self.shoots.remove(shoot)  # for removing object from list
                return True

        for shot in self.shots:
            if shot.id == r_id:
                shot.remove_self()
                self.shots.remove(shot)  # for removing object from list
                return True
        return False

    def update_record(self, r_id, name):
        """Method to updating record that has given id.

        Args:
            r_id (str):               ID of the record.
            name (str):             The name of the record.
        """

        for shoot in self.shoots:
            if shoot.id == r_id:
                shoot.update_name(name)
                return True

        for shot in self.shots:
            if shot.id == r_id:
                shot.update_name(name)
                return True

        return False

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.records_folder):
            os.mkdir(self.records_folder)


class Shoot:
    """Class to define records of t_systems vision.

    This class provides necessary initiations and functions named :func:`t_system.recordation.Record.__db_upsert`
    for saving records to the database safely.
    """

    def __init__(self, d_m_y, h_m_s, scope, record_formats, id=None, name=None, length=None):
        """Initialization method of :class:`t_system.recordation.Record` class.

        Args:
                d_m_y (str):            Date that is day_mount_year format.
                h_m_s (str):            Date that is hour_minute_second format.
                scope (str):            The working type during recording.
                record_formats (dict):  Formats of the records for video, audio and merged.
                id (str):               The id of the record.
                name (str):             The name of the record.
                length (str):           The length of the record as m:s.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        if not name:
            self.name = h_m_s

        self.date = d_m_y  # table name at the same time
        self.time = h_m_s
        self.scope = scope
        self.record_formats = record_formats
        self.length = length

        self.records_folder = f'{dot_t_system_dir}/records'
        self.parent_folder = f'{self.records_folder}/{self.date}'
        self.folder = f'{self.parent_folder}/{self.time}'

        self.video_file = f'{self.folder}/{self.time}.{self.record_formats["video"]}'
        self.audio_file = f'{self.folder}/{self.time}.{self.record_formats["audio"]}'
        self.merged_file = f'{self.folder}/{self.time}.{self.record_formats["merged"]}'

        self.table = DBFetcher(self.records_folder, "db", "shoots").fetch()

        self.__check_folders()

        if length is None:
            self.length = self.__calc_length()

        self.__db_upsert()

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):        Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().id == self.id)):
            if force_insert:
                # self.already_exist = False
                self.table.update({'id': self.id, 'name': self.name, 'time': self.time, 'date': self.date, 'scope': self.scope, 'record_formats': self.record_formats, 'length': self.length}, Query().id == self.id)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'time': self.time,
                'date': self.date,
                'scope': self.scope,
                'record_formats': self.record_formats,
                'length': self.length
            })  # insert the given data

        return ""

    def update_name(self, name):
        """Method to updating self name via by given parameter.

        Args:
            name (str):                 The name of the record.
        """

        self.name = name
        self.__db_upsert(True)

    def remove_self(self):
        """Method to remove face itself.
        """

        rmtree(self.folder)

        self.table.remove((Query().id == self.id))

    def __calc_length(self):
        """Method to calculating length of record with using OpenCV.
        """
        if os.path.exists(self.merged_file):
            import cv2

            cap = cv2.VideoCapture(self.merged_file)

            fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = frame_count / fps

            minutes = int(duration / 60)
            seconds = round(duration % 60)
            length = f'{minutes}:{seconds}'

            cap.release()

            return length

        return None

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)


class Shot:
    """Class to define shots of t_systems vision.

    This class provides necessary initiations and functions named :func:`t_system.recordation.Shot.__db_upsert`
    for saving shots to the database safely.
    """

    def __init__(self, d_m_y, h_m_s, shot_format, id=None, name=None, size=None):
        """Initialization method of :class:`t_system.recordation.Record` class.

        Args:
                d_m_y (str):            Date that is day_mount_year format.
                h_m_s (str):            Date that is hour_minute_second format.
                shot_format (str):      Format of the shot. (jpg, png etc.)
                id (str):               The id of the record.
                name (str):             The name of the record.
                size (str):           The length of the record as m:s.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        if not name:
            self.name = h_m_s

        self.date = d_m_y  # table name at the same time
        self.time = h_m_s
        self.shot_format = shot_format
        self.size = size

        self.records_folder = f'{dot_t_system_dir}/records'
        self.parent_folder = f'{self.records_folder}/{self.date}'
        self.folder = f'{self.parent_folder}/{self.time}'

        self.shot_file = f'{self.folder}/{self.time}.{self.shot_format}'

        self.table = DBFetcher(self.records_folder, "db", "shots").fetch()

        self.__check_folders()

        if size is None:
            self.size = self.__calc_size()

        self.__db_upsert()

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):        Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().id == self.id)):
            if force_insert:
                # self.already_exist = False
                self.table.update({'id': self.id, 'name': self.name, 'time': self.time, 'date': self.date, 'shot_format': self.shot_format, 'size': self.size}, Query().id == self.id)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'time': self.time,
                'date': self.date,
                'shot_format': self.shot_format,
                'size': self.size
            })  # insert the given data

        return ""

    def update_name(self, name):
        """Method to updating self name via by given parameter.

        Args:
            name (str):                 The name of the record.
        """

        self.name = name
        self.__db_upsert(True)

    def remove_self(self):
        """Method to remove face itself.
        """

        rmtree(self.folder)

        self.table.remove((Query().id == self.id))

    def __calc_size(self):
        """Method to calculating length of record with using OpenCV.
        """
        if os.path.exists(self.shot_file):

            return os.path.getsize(self.shot_file) / 1000  # in kB unit.

        return None

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
