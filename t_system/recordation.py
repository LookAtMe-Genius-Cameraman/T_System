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

from t_system import dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class Recorder:
    """Class to define a recording ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.audition.Audition.listen_async`
    as the loop for asynchronous collecting audio data to the vision ability, named :func:`t_system.audition.Audition.listen_sync`
    for the synchronous collecting audio data to the vision ability and named :func:`t_system.audition.Audition.start_recording`
    as entry point from vision ability for starting recording processes.
    """

    def __init__(self, camera, hearer):
        """Initialization method of :class:`t_system.recordation.Recorder` class.

        Args:
                camera:       	        Camera object from PiCamera.
                hearer:       	        Hearer object.
        """
        self.record_path = dot_t_system_dir + "/records"

        if not os.path.exists(self.record_path):
            os.mkdir(self.record_path)

        self.record_video_name = ""
        self.record_audio_name = ""
        self.final_record_file = ""

        self.camera = camera
        self.hearer = hearer
    
    def start(self, mode="track", video_format="h264", audio_format="wav", final_format="mkv"):
        """The low-level method to start audio and video recording asynchronously.

         Args:
                mode:       	        The running mode which is wants to set video name.
                video_format:       	The video output format either 'h264' or 'mjpeg'. Other options in library are for raw data.
                audio_format:       	The video output format. Allowed format is 'wav'.
                final_format:       	The final recording format after audio and video files merged.
        """

        self.set_record_name(mode, video_format, audio_format, final_format)
        self.camera.start_recording(self.record_video_name, video_format)

        self.hearer.start_recording(self.record_audio_name, audio_format)

    def stop(self):
        """The low-level method to stop audio and video recording
        """

        self.camera.stop_recording()
        self.hearer.stop_recording()

    def merge_audio_and_video(self):
        """The low-level method to merge recorded audio and video files.
        """
        merge_cmd = 'ffmpeg -y -i ' + self.record_audio_name + ' -r 24 -i ' + self.record_video_name + ' -filter:a aresample=async=1 -c:a flac -c:v copy av.mkv'
        subprocess.call(merge_cmd, shell=True)
        logger.info('Video and Audio Muxing Done')

    def set_record_name(self, mode, video_format="h264", audio_format="wav", final_format="mkv"):
        """The low-level method to prepare the name of recording video with its path.

         Args:
                mode:       	        The running mode which is wants to set video name.
                video_format:       	The video output format either 'h264' or 'mjpeg'. Other options in library are for raw data.
                audio_format:       	The audio output format. Allowed format is 'wav'.
                final_format:       	The final recording format after audio and video files merged.
        """
        common = self.record_path + "/" + mode + "_" + datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + "."

        self.record_video_name = common + video_format  # name looks like: PATH/22-05-2019_19:08:12.h264
        self.record_audio_name = common + audio_format  # name looks like: PATH/22-05-2019_19:08:12.wav
        self.final_record_file = common + final_format  # name looks like: PATH/22-05-2019_19:08:12.mkv
