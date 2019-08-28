#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: action
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to setting predicted positions and creating scenarios ability for T_System's robotic arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import uuid  # The random id generator

from multipledispatch import dispatch

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system.motion.arm import Arm
from t_system.db_fetching import DBFetcher

from t_system import dot_t_system_dir, T_SYSTEM_PATH


class ActionManager:
    """Class to define action manager to managing movements of Arm and Locking System (when it is using independent from seer during tracking non-moving objects).

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Action_Manager.`
        for the provide move of servo motor.

    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.motion.action.ActionManager` class.

        Args:
            args:                   Command-line arguments.
        """

        self.predicted_actions_db = f'{T_SYSTEM_PATH}/motion/action/predicted_actions.json'
        self.actions_db = dot_t_system_dir + "/actions.json"


class Actor:
    """Class to define an actor to fulfill tasks with given positions and scenarios.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Actor.`
        for the provide move of servo motor.

    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.motion.action.Actor` class.

        Args:
            args:                   Command-line arguments.
        """

        self.arm = None
        if args["robotic_arm"]:
            self.arm = Arm(args["robotic_arm"])

    @dispatch(object)
    def act(self, position):
        """Method to moving by given position object.

        Args:
            position (Position):            A Position object
        """

        self.arm.goto_position(pos_thetas=position.polar_coords, pos_coords=position.cartesian_coords)

    @dispatch(list)
    def act(self, scenarios):
        """Method to moving by given position object.

        Args:
            scenarios (list):"              Scenario object list
        """

        for scenario in scenarios:
            for position in scenario.positions:
                self.arm.goto_position(pos_thetas=position.polar_coords, pos_coords=position.cartesian_coords)


class Scenario:
    """Class to define scenarios via creating path with given positions.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Scenario.add_positions`
        for the provide entry point to adding new positions to the scenario.

    """

    def __init__(self, name, id=None, root=False):
        """Initialization method of :class:`t_system.motion.action.Scenario` class.

        Args:
            id (str):                       The id of the scenario.
            name (str):                     The name of the scenario.
            root (bool):                    Root privileges flag.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        self.positions = []
        self.root = root

        if self.root:
            db_folder = f'{T_SYSTEM_PATH}/motion/action'
            db_name = 'predicted_actions'
            self.table = self.__get_db(db_folder, db_name, 30)
        else:
            db_folder = dot_t_system_dir
            db_name = 'actions'
            self.table = self.__get_db(db_folder, db_name)

        self.refresh_positions()

    def add_positions(self, positions):
        """Method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """

        self.positions.extend(positions)
        self.db_upsert()

    def delete_positions(self, positions):
        """Method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """

        for position in positions:
            self.positions.remove(position)

        self.db_upsert(force_insert=True)

    def delete_self(self):
        """Method to delete scenario itself.
        """
        self.table.remove((Query().name == self.name))

    def db_upsert(self, force_insert=False):
        """Function to insert(or update) the position to the database.

        Args:
            force_insert (bool):           force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().name == self.name)):
            if force_insert:
                self.table.update({'name': self.name, 'positions': self.positions}, Query().id == self.id)

            else:
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'positions': [{
                    "id": position.id,
                    "name": position.name,
                    "cartesian_coords": position.cartesian_coords,
                    "polar_coords": position.polar_coords
                } for position in self.positions]
            })  # insert the given data

        return ""

    @staticmethod
    def __get_db(db_folder, db_name, cache_size=None):
        """Function to set the database of the scenario.

        Args:
            db_folder (str):                Containing folder of the database file
            db_name (str):                  Database file of the scenario abject.
            cache_size (int):               TinyDB caches query result for performance.
        """

        return DBFetcher(db_folder, db_name, "scenarios", cache_size).fetch()

    def refresh_positions(self):
        """low-level method to refreshing the members
        """

        scenarios = self.table.search((Query().id == self.id))
        for position in scenarios["positions"]:
            self.positions.append(Position(position["name"], position["id"], position["cartesian_coords"], position["polar_coords"], self.root, is_for_scenario=True))


class Position:
    """Class to define the position of the arm with cartesian coordinates of arms' last point and angle value of its joints.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Position.update_coords`
        for updating utilities of itself.

    """

    def __init__(self, name, id=None, cartesian_coords=None, polar_coords=None, root=False, is_for_scenario=False):
        """Initialization method of :class:`t_system.motion.arm.action.Position` class.

        Args:
            name (str):                     The name of the position.
            id (str):                       The id of the position.
            cartesian_coords (list):        Cartesian coordinate value list of the position.
            polar_coords (list):            Polar coordinate value list of the position.
            root (bool):                    Root privileges flag.
            is_for_scenario (bool):        Flag that is specified position is inside a scenario.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        self.cartesian_coords = cartesian_coords
        self.polar_coords = polar_coords
        self.root = root
        self.is_for_scenario = is_for_scenario

        if self.root:
            db_folder = f'{T_SYSTEM_PATH}/motion/action'
            db_name = 'predicted_actions'
            self.table = self.__get_db(db_folder, db_name, 30)
        else:
            db_folder = dot_t_system_dir
            db_name = 'actions'
            self.table = self.__get_db(db_folder, db_name)

        self.db_upsert()

    def update_coords(self, cartesian_coords, polar_cords):
        """Method to updating self coordinates via by given parameters.

        Args:
            cartesian_coords (list):        Cartesian coordinate value list of the position.
            polar_cords (list):             Polar coordinate value list of the position.
        """

        self.cartesian_coords = cartesian_coords
        self.polar_coords = polar_cords

        self.db_upsert(force_insert=True)

    def delete_self(self):
        """Method to delete position itself.
        """
        self.table.remove((Query().name == self.name))

    def db_upsert(self, force_insert=False):
        """Function to insert(or update) the position to the database.

        Args:
            force_insert (bool):           force insert flag.

        Returns:
            str:  Response.
        """

        if not self.is_for_scenario:
            if self.table.search((Query().name == self.name)):
                if force_insert:
                    self.table.update({'name': self.name, 'cartesian_coords': self.cartesian_coords, 'polar_cords': self.polar_coords}, Query().id == self.id)

                else:
                    return "Already Exist"
            else:
                self.table.insert({
                    'id': self.id,
                    'name': self.name,
                    'cartesian_coords': self.cartesian_coords,
                    'polar_cords': self.polar_coords
                })  # insert the given data

        return ""

    def __get_db(self, db_folder, db_name, cache_size=30):
        """Function to set the database of the position.

        Args:
            db_folder (str):                Containing folder of the database file
            db_name (str):                  Database of the position abject.
            cache_size (int):               TinyDB caches query result for performance.
        """

        if self.is_for_scenario:
            return DBFetcher(db_folder, db_name, "scenarios", cache_size).fetch()
        else:
            return DBFetcher(db_folder, db_name, "positions", cache_size).fetch()


if __name__ == '__main__':

    position_demonstration = Position("go_to_home", cartesian_coords=[1.5, 1.5, 1.5], root=True)


