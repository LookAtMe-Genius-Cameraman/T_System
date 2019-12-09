#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: record
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for handling video records of T_System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import os
import base64

from t_system import log_manager
from t_system import record_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def get_record_dates(admin_id):
    """Method to return existing positions.

    Args:
            admin_id (str):                 Root privileges flag.
    """
    try:
        result = record_manager.get_record_dates()
    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_records(admin_id, records_date):
    """Method to return existing position with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            records_date (str):             Date of the wanted records.
    """
    result = {"shoots": [], "shots": []}

    shoots = record_manager.get_records("shoot", records_date)
    shots = record_manager.get_records("shot", records_date)

    if shoots:
        for shoot in shoots:
            result["shoots"].append({"id": shoot.id, "name": shoot.name, "time": shoot.time, "length": shoot.length, "extension": shoot.record_formats["merged"]})

    if shots:
        for shot in shots:
            result["shots"].append({"id": shot.id, "name": shot.name, "time": shot.time, "size": shot.size, "extension": shot.shot_format})

    return result


def get_record(admin_id, record_id):
    """Method to return existing position with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            record_id (str):                The id of the record.
    """

    record, r_type = record_manager.get_record(record_id)

    if not record:
        return None, None
    if r_type == "shoot":
        return open(record.merged_file, 'rb'), f'video/{record.record_formats["merged"]};'

    elif r_type == "shot":
        return open(record.shot_file, 'rb'), f'image/{record.shot_format};'


def download_record(admin_id, record_id):
    """Method to return existing face and copying its images under the static folder with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            record_id (str):                The id of the record.
    """

    record, r_type = record_manager.get_record(record_id)

    if record:
        if r_type == "shoot":
            return record.merged_file, f'{record.name}.{record.record_formats["merged"]}'

        elif r_type == "shot":
            return record.shot_file, f'{record.name}.{record.shot_format}'

    return None


def update_record(admin_id, record_id, data):
    """Method to remove existing position with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            record_id (str):                The id of the record.
            data (dict):                    Record data structure.
    """

    result = record_manager.update_record(record_id, data["name"])

    return result


def delete_record(admin_id, record_id):
    """Method to remove existing position with given id.

    Args:
            admin_id (str):                 Root privileges flag.
            record_id (str):                The id of the record.
    """

    result = record_manager.delete_record(record_id)

    return result
