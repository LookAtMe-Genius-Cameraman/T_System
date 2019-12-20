#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: live_stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for Live Stream ability of T_System Vision.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system.administration import is_admin

from t_system import seer

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def switch_live_stream(admin_id, in_use):
    """Method to start / stop live streaming.

    Args:
            admin_id (str):                 Admin privileges flag.
            in_use (bool):                  usage status flag.
    """

    try:
        if in_use:
            seer.online_streamer.go_live()
        else:
            seer.online_streamer.stop_live()

        return True
    except Exception as e:
        logger.error(e)
        return False


def set_stream_id_u_status(admin_id, website_id, account_name, in_use):
    """Method to set usage status of live stream's a stream ID of a website.

    Args:
            admin_id (str):                 Admin privileges flag.
            website_id (str):               The id of the position.
            account_name (str):             Name of the website's account.
            in_use (str):                  usage status flag.
    """

    in_use = in_use in ["true", "True"]

    return seer.online_streamer.activate_website_stream(website_id, account_name)


def set_website_usage_status(admin_id, website_id, in_use):
    """Method to set usage status of live stream's websites.

    Args:
            admin_id (str):                 Admin privileges flag.
            website_id (str):               The id of the position.
            in_use (str):                  usage status flag.
    """
    in_use = in_use in ["true", "True"]

    if not is_admin(admin_id):
        return False

    return seer.online_streamer.set_website_usage_stat(website_id, in_use)


def create_stream_id(admin_id, root, website_id, data):
    """Method to create new stream ID for given website.

    Args:
            admin_id (str):                 Admin privileges flag.
            root (str):                     Root privileges activation flag.
            website_id (str):               The id of the position.
            data (dict):                    Stream ID data structure.
    """

    try:

        result = seer.online_streamer.set_website_stream(website_id, data)

    except Exception:
        result = False

    return result


def update_stream_id(admin_id, root, website_id, data):
    """Method to update the Stream ID of given website.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            website_id (str):               The id of the website.
            data (dict):                    Stream ID data structure.
    """

    return seer.online_streamer.set_website_stream(website_id, data)


def delete_stream_id(admin_id, root, website_id, account_name):
    """Method to remove existing website with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            website_id (str):               The id of the website.
            account_name (str):             Name of the website's account.
    """

    return seer.online_setreamer.remove_website_stream(website_id, account_name)


def upsert_website(admin_id, root, data, force_insert=False):
    """Method to update and insert new website to live streaming.

    Args:
            admin_id (str):                 Admin privileges flag.
            root (str):                     Root privileges activation flag.
            data (dict):                    website data structure.
            force_insert (bool):            Force insert Flag for updating the website information.
    """

    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        if root:
            result = seer.online_streamer.add_website(data["name"], data["url"], data["server"], force_insert=force_insert)
        else:
            result = False

    except Exception:
        result = False

    return result


def get_websites(admin_id, root):
    """Method to return existing websites.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
    """
    result = []
    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        websites = seer.online_streamer.get_websites()

        if websites:
            for website in websites:
                result.append({"id": website.id, "name": website.name, "url": website.url, "server": website.server, "to_be_used": website.to_be_used, "stream_ids": website.stream_ids})

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_website(admin_id, root, website_id):
    """Method to return existing website with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            website_id (str):               The id of the position.
    """
    result = []

    try:
        if not is_admin(admin_id):
            root = False
        else:
            root = root in ["true", "True"]

        websites = seer.online_streamer.get_websites(w_ids=[website_id])

        if websites:
            for website in websites:
                result.append({"id": website.id, "name": website.name, "url": website.url, "server": website.server, "to_be_used": website.to_be_used, "stream_ids": website.stream_ids})

    except Exception as e:
        logger.error(e)
        result = []

    return result


def delete_website(admin_id, root, website_id):
    """Method to remove existing website with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            root (str):                     Root privileges activation flag.
            website_id (str):               The id of the website.
    """
    if not is_admin(admin_id):
        root = False
    else:
        root = root in ["true", "True"]

    if root:
        result = seer.online_setreamer.remove_websites([website_id])
    else:
        result = False

    return result
