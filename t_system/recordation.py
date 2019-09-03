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

    def __init__(self, record_formats, camera, hearer):
        """Initialization method of :class:`t_system.recordation.Recorder` class.

        Args:
                record_formats (list):  Formats of the records for video, audio and merged.
                camera:       	        Camera object from PiCamera.
                hearer:       	        Hearer object.
        """

        self.current_video_file = ""
        self.current_audio_file = ""
        self.current_merged_file = ""

        self.record_formats = {"video": record_formats[0], "audio": record_formats[1], "merged": record_formats[2]}

        self.camera = camera
        self.hearer = hearer
    
    def start(self, mode="track"):
        """Method to start audio and video recording asynchronously.

         Args:
                mode:       	        The running mode which is wants to set video name.
        """

        record = Record(datetime.datetime.now().strftime("%d_%m_%Y"), datetime.datetime.now().strftime("%H_%M_%S"), mode, self.record_formats)

        self.__set_record_params(record)

        self.camera.start_recording(self.current_video_file, self.record_formats["video"])
        self.hearer.start_recording(self.current_audio_file, self.record_formats["audio"])

    def stop(self):
        """Method to stop audio and video recording
        """

        self.camera.stop_recording()
        self.hearer.stop_recording()

        # Todo: This is disgusting way to merging audio and silent video. Fix this.
        self.merge_audio_and_video()

    def merge_audio_and_video(self):
        """Method to merge recorded audio and video files.
        """

        merge_cmd = f'ffmpeg -y -i {self.current_audio_file} -r 24 -i {self.current_video_file} -filter:a aresample=async=1 -c:a flac -c:v copy {self.current_merged_file}'
        subprocess.call(merge_cmd, shell=True)
        logger.info('Video and Audio Muxing Done')

    def __set_record_params(self, record):
        """Method to setting current parameter by current recording.
        """

        self.current_video_file = record.video_file
        self.current_audio_file = record.audio_file
        self.current_merged_file = record.merged_file


class RecordManager:
    """Class to define Record manager for handling the recordation database of t_system's vision.

    This class provides necessary initiations and functions named :func:`t_system.recordation.RecordManager.get_records`
    for returning the Record objects of existing records with given table(date at the same time) parameter.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.recordation.RecordManager` class.
        """

        self.records_folder = f'{dot_t_system_dir}/records'

        if not os.path.exists(self.records_folder):
            os.mkdir(self.records_folder)

        self.db = DBFetcher(self.records_folder, "db").fetch()

        self.table_names = list(self.db.tables())
        self.tables = []

        self.records = []

        self.__set_tables()
        self.__set_records()

    def __set_tables(self):
        """Method to set table of record database.
        """

        for table_name in self.table_names:
            self.tables.append(DBFetcher(self.records_folder, "db", table_name).fetch())

    def __set_records(self):
        """Method to set existing records.
        """

        for table in self.tables:
            for record in table.all():
                self.records.append(Record(record["parent_name"], record["name"], record["scope"], record["record_formats"]))

    def get_records(self, table_name):
        """Method to get existing records in given table name. If table is None it returns all records.
        """
        records = []

        if table_name:
            for record in self.records:
                if record.parent_name == table_name:
                    records.append(record)
            return records

        return self.records


class Record:
    """Class to define records of t_systems vision.

    This class provides necessary initiations and functions named :func:`t_system.recordation.Record.__db_upsert`
    for saving records to the database safely.
    """

    def __init__(self, d_m_y, h_m_s, scope, record_formats):
        """Initialization method of :class:`t_system.recordation.Record` class.

        Args:
                d_m_y (str):            Date that is day_mount_year format.
                h_m_s (str):            Date that is hour_minute_second format.
                scope (str):            The working type during recording.
                record_formats (dict):  Formats of the records for video, audio and merged.
        """

        self.parent_name = d_m_y  # table name at the same time
        self.name = h_m_s
        self.scope = scope
        self.record_formats = record_formats
        self.length = 0.0  # in seconds

        self.records_folder = f'{dot_t_system_dir}/records'
        self.parent_folder = f'{self.records_folder}/{self.parent_name}'
        self.folder = f'{self.parent_folder}/{self.name}'
        self.__check_folders()

        self.table = DBFetcher(self.records_folder, "db", self.parent_name).fetch()

        self.video_file = f'{self.folder}.{self.name}.{self.record_formats["video"]}'
        self.audio_file = f'{self.folder}.{self.name}.{self.record_formats["audio"]}'
        self.merged_file = f'{self.folder}.{self.name}.{self.record_formats["merged"]}'

        self.__db_upsert()

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().name == self.name)):
            if force_insert:
                # self.already_exist = False
                self.table.update({'name': self.name, 'parent_name': self.parent_name, 'scope': self.scope, 'record_formats': self.record_formats, 'length': self.length}, Query().name == self.name)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'name': self.name,
                'parent_name': self.parent_name,
                'scope': self.scope,
                'record_formats': self.record_formats,
                'length': self.length
            })  # insert the given data

        return ""

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
