#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's video and audio stream.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import seer


def start_stream(admin_id, stream_type):
    """The high-level method to return existing position with given id.

    Args:
        admin_id (bool):                 Root privileges flag.
        stream_type (str):               Stream's purpose. Preview, track-learn mode etc.
    """
    try:
        seer.start_online_stream()
        if stream_type == "preview":

            return seer.stream(stop_thread=lambda: False, caller="preview"), "multipart/x-mixed-replace; boundary=frame"

    except Exception as e:
        print(e)

    return False, False


def stop_stream(admin_id):
    """The high-level method to remove existing position with given id.

    Args:
        admin_id (bool):                 Root privileges flag.
        position_id (str):              The id of the position.
    """

    try:
        seer.stop_online_stream()
    except Exception as e:
        print(e)


    # table = get_db_table(is_admin(admin_id))
    #
    # if table.search((Query().id == position_id)):
    #     table.remove((Query().id == position_id))
    #
    #     result = True
    # else:
    #     result = False

    # return result
    pass
