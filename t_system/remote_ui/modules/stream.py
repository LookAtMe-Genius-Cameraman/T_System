#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's video and audio stream.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import threading

from t_system import seer


class StreamManager:
    """Class to define a manager for asynchronous work of t_system's online video stream.

        This class provides necessary initiations and a function named
        :func:`t_system.remote_ui.modules.stream.StreamManager.get_stream`
        for the provide getting stream by calling iteratively the seer's current_frame member.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.remote_ui.modules.stream.StreamManager` class.
        """

        self.stop_thread = False
        self.preview_thread = threading.Thread(target=seer.stream, args=(lambda: self.stop_thread, "bgr", "preview"))

    def start_stream(self, admin_id, stream_type):
        """The high-level method to return existing position with given id.

        Args:
            admin_id (bool):                 Root privileges flag.
            stream_type (str):               Stream's purpose. Preview, track-learn mode etc.
        """
        try:
            if stream_type == "preview":
                self.preview_thread.start()
                return self.get_stream(), "multipart/x-mixed-replace; boundary=frame"

        except Exception as e:
            print(e)

        return False, False

    def stop_stream(self, admin_id, stream_type):
        """The high-level method to remove existing position with given id.

        Args:
            admin_id (bool):                 Root privileges flag.
            stream_type (str):               Stream's purpose. Preview, track-learn mode etc.
        """
        result = True
        try:
            if stream_type == "preview" and self.preview_thread.is_alive():
                self.stop_thread = True
                self.preview_thread.join()

        except Exception as e:
            print(e)
            result = False

        return result

    @staticmethod
    def get_stream():
        """The low-level method to get camera stream frame by frame from seer.current_frame.
        """
        while True:
            frame = seer.get_current_frame()
            if frame is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')

