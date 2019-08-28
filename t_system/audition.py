#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: audition
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's audition ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import pyaudio  # Provides Python bindings for PortAudio, the cross platform audio API
import sys  # System-specific parameters and functions
import datetime  # Basic date and time types
import wave
import threading

from t_system import dot_t_system_dir


class Hearer:
    """Class to define an audition of tracking system..

    This class provides necessary initiations and functions named :func:`t_system.audition.Audition.__listen_async`
    as the loop for asynchronous collecting audio data to the vision ability, named :func:`t_system.audition.Audition.listen_sync`
    for the synchronous collecting audio data to the vision ability and named :func:`t_system.audition.Audition.start_recording`
    as entry point from vision ability for starting recording processes.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.audition.Hearer` class.

        Args:
                args:                   Command-line arguments.
        """
        self.chunk = args["chunk"]
        self.format = pyaudio.paInt16  # Data format, 16-bit resolution.
        self.rate = args["rate"]
        self.channels = args["channels"]
        self.input_device_index = args["audio_device_index"]

        self.record = args["record"]
        self.record_path = ""
        self.record_name = ""

        self.record_format = "wav"

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate, input=True, input_device_index=self.input_device_index, frames_per_buffer=self.chunk)

        self.frames = []

        self.listen_thread_stop = False
        self.listen_thread = threading.Thread(target=self.__listen_async, args=(lambda: self.listen_thread_stop,))

    def start_recording(self, record_name, format="wav"):
        """Method to start audio recording.

        Args:
                record_name:   	        The name of  the recording file with its path.
                format:       	        The audio output format.
        """
        self.__set_record_path()  # this is dysfunctional
        self.record_name = record_name

        self.listen_thread.start()

    def stop_recording(self):
        """Method to stop audio recording.
        """
        self.listen_thread_stop = True
        self.listen_thread.join()

        self.__save_frames()
        self.frames.clear()

    def __listen_async(self, stop):
        """Method to provide listening ability physical around of t_system as asynchronous to vision its ability. Powered by multi threading method.

        Args:
                stop:       	    Stop flag of the tread about terminating it outside of the function's loop.
        """
        while True:
            if stop():
                self.__stop_stream()
                break
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def listen_sync(self):
        """Method to provide listening ability physical around of t_system as synchronous to vision its ability.

            Camera recording rate is about 24 fps. That mean there is 24 frame in second.
            If self.rate is constant, chunk =  self.rate * record_seconds / frame_length = 44100 * 1 / 24 = 1837
        """

        chunk = 1837.5
        data = self.stream.read(chunk)
        self.frames.append(data)

    def __save_frames(self):
        """Method to save collected data frames to the file after recording.
        """

        wav_file = wave.open(self.record_name, 'wb')
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(self.audio.get_sample_size(self.format))
        wav_file.setframerate(self.rate)
        wav_file.writeframes(b''.join(self.frames))
        wav_file.close()

    def __set_record_path(self):
        """Method to prepare the name of recording audio with its path.
        """
        self.record_path = dot_t_system_dir

    def __stop_stream(self):
        """Method to provide stop the audio stream.
        """
        self.stream.__stop_stream()  # "Pause the Stream"

    def release_members(self):
        """Method to provide close the audio stream and terminate the PyAudio object.
        """

        self.stream.close()  # "Stream Stop"
        self.audio.terminate()



