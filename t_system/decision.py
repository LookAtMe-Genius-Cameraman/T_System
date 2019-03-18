#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: decision
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's decision ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from os.path import expanduser  # Imported to get the home directory

import numpy

initial_k_fact = 0.01
acceptable_err_rate = 5.0


class Decider():
    """Class to provide the k factor decision ability.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.Decider` class.
        """

        home = expanduser("~")  # Get the home directory of the user
        self.db = TinyDB(home + '/.t_system_db.json')  # This is where we store the database; /home/USERNAME/.t_system_db.json

    def decision(self, obj_width, err_rate=100.0, is_err_check=False):
        """Function to decide the necessary k factor with a kind of AI method.

        Args:
            obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            err_rate (float):        % error rate. Difference between target point and reached point. ((target point - end point) / (target point - start point)*100)
            is_err_check:            Control point for the second usage of `t_system.Decider.decision` to determine the error rate after angular moving.
        Returns:
            int:              k factor.
        """

        err_rate = abs(err_rate)

        result = {}
        if self.db.search((Query().obj_width == obj_width)):
            result = self.db.search((Query().obj_width == obj_width))[0]  # There is just 1 return value so, index 0 will be enough.

        if not is_err_check:
            if result:
                if result['err_rate'] <= acceptable_err_rate:
                    return result['k_fact']
                else:
                    return result['next_k_fact']
            else:
                self.db_upsert(initial_k_fact, obj_width, err_rate, initial_k_fact)
                return initial_k_fact
        else:
            if result:
                if (err_rate < result['err_rate']) and (result['err_rate'] > acceptable_err_rate):  # if current error rate smaller than the last one and last error rate bigger than acceptable range, determine new k factor.
                    # FOR MAKING A DECISION TO NEXT K FACTOR.
                    accur_rate = 1 - err_rate / 100
                    next_k_fact = result['k_fact'] / accur_rate

                    self.db_upsert(result['next_k_fact'], obj_width, err_rate, next_k_fact)

                elif (err_rate < result['err_rate']) and (result['err_rate'] <= acceptable_err_rate):  # if current error rate smaller than the last one but last error rate smaller than acceptable range, use the same k factor.
                    self.db_upsert(result['k_fact'], obj_width, err_rate, result['k_fact'])

                elif err_rate > result['err_rate']:  # if current error rate bigger than the last one, try to learn k factor again from the begining.
                    self.db_upsert(initial_k_fact, obj_width, 100, initial_k_fact)

    # def db_get(self, obj_width):
    #     """Function to get a note record from the database.  NOT COMPLETED.
    #
    #     Args:
    #         obj_width (int):  Width of the finded object for measurement inferencing.
    #
    #     Returns:
    #         int:              k_fact and error rate.
    #     """
    #
    #     result = self.db.search((Query().obj_width == obj_width))[0]
    #     if result:
    #         return result['k_fact'], result['err_rate'], result['next_k_fact']
    #     else:
    #         return None

    def db_upsert(self, k_fact, obj_width, err_rate, next_k_fact):
        """Function to insert(or update) a note record to the database.

        Args:
            k_fact (float):          The factor related to object width for measurement inferencing.
            obj_width (int):         Width of the found object from haarcascade for measurement inferencing.
            err_rate (float):        % error rate. Difference between target point and reached point. ((target point - end point) / (target point - start point)*100)
            next_k_fact (float)      If the aplied k_fact's error rate bigger than %5, try this decided k_fact.
        Returns:
            str:  Response.
        """

        if isinstance(next_k_fact, numpy.float):
            next_k_fact = float(next_k_fact)

        if self.db.search((Query().obj_width == obj_width)):
            self.db.update({'k_fact': k_fact, 'err_rate': err_rate, 'next_k_fact': next_k_fact}, Query().obj_width == obj_width)
        else:
            self.db.insert({
                'obj_width': int(obj_width),
                'k_fact': k_fact,
                'err_rate': err_rate,
                'next_k_fact': next_k_fact
            })  # insert the given data

        return ""

    # def db_delete(self, note=None, category=None, are_all=False, list_name=None, list_sequence=None, is_todolist=False, is_reminder=False, is_active=False, is_public=True, user_id=None):
    #     """Function to delete a note record from the database.  NOT COMPLETED.
    #
    #     Args:
    #         note (str):  note that extracted from the user's input/command.
    #
    #     Keyword Args:
    #         is_reminder (int):  Is it a note for remind? (default: False)
    #         is_public (int):    Is it a public record? (non-user specific)
    #         user_id (int):      User's ID.
    #
    #     Returns:
    #         str: Response.
    #     """
    #
    #     if are_all:
    #         self.db.remove((Query().is_todolist == is_todolist) | (Query().is_reminder == is_reminder))  # ?f added the "to do list for remind" to the future, this line will be reworked.
    #         return ""
    #     if self.db.remove((Query().is_todolist == is_todolist) & (Query().is_reminder == is_reminder)):
    #         return ""
    #     else:
    #         return "There is no note."

