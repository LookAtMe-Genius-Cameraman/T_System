#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: action
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to setting predicted positions and creating scenarios ability for T_System's robotic arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import uuid  # The random id generator

from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system import dot_t_system_dir, T_SYSTEM_PATH

predicted_actions_db = f'{T_SYSTEM_PATH}/motion/arm/predicted_actions.json'


class Position:
    """Class to define the position of the arm with cartesian coordinates of arms' last point and angle value of its joints.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, name, id=None, cartesian_coords=None, polar_coords=None, root=False):
        """Initialization method of :class:`t_system.motion.arm.action.Position` class.

        Args:
            name (str):                     The name of the position.
            id (str):                       The id of the position.
            cartesian_coords (list):        Cartesian coordinate value list of the position.
            polar_coords (list):            Polar coordinate value list of the position.
            root (bool):                    Root privileges flag.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        self.cartesian_coords = cartesian_coords
        self.polar_coords = polar_coords

        self.table = None

        if root:
            self.set_db(cache_size=30)
        else:
            actions_db = dot_t_system_dir + "/actions.json"
            self.set_db(actions_db)

        self.db_upsert()

    def update_coords(self, cartesian_coords, polar_cords):
        """The low-level method to add position to the scenario.

        Args:
            cartesian_coords (list):        Cartesian coordinate value list of the position.
            polar_cords (list):             Polar coordinate value list of the position.
        """

        self.cartesian_coords = cartesian_coords
        self.polar_coords = polar_cords

        self.db_upsert(force_insert=True)

    def delete_self(self):
        """The high-level method to delete scenario itself.
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
                # self.already_exist = False
                self.table.update({'name': self.name, 'cartesian_coords': self.cartesian_coords, 'polar_cords': self.polar_coords}, Query().id == self.id)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'cartesian_coords': self.cartesian_coords,
                'polar_cords': self.polar_coords
            })  # insert the given data

        return ""

    def set_db(self, db_file=predicted_actions_db, cache_size=30):
        """Function to set the database of the position.

        Args:
            db_file (str):                  Database of the position abject.
            cache_size (int):               TinyDB caches query result for performance.
        """

        db = TinyDB(db_file)
        self.table = db.table("positions", cache_size=cache_size)


class Scenario:
    """Class to define scenarios via creating path with given positions.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, name, id=None, root=False):
        """Initialization method of :class:`t_system.motion.arm.action.Scenario` class.

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

        self.table = None

        if root:
            self.set_db(cache_size=30)
        else:
            actions_db = dot_t_system_dir + "/actions.json"
            self.set_db(actions_db)

    def add_positions(self, positions):
        """The low-level method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """

        self.positions.extend(positions)
        self.db_upsert()

    def delete_positions(self, positions):
        """The low-level method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """

        for position in positions:
            self.positions.remove(position)

        self.db_upsert(force_insert=True)

    def delete_self(self):
        """The high-level method to delete scenario itself.
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
                # self.already_exist = False
                self.table.update({'name': self.name, 'positions': self.positions}, Query().id == self.id)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'positions': self.positions
            })  # insert the given data

        return ""

    def set_db(self, db_file=predicted_actions_db, cache_size=None):
        """Function to set the database of the scenario.

        Args:
            db_file (str):                  Database of the position abject.
            cache_size (int):               TinyDB caches query result for performance.
        """

        db = TinyDB(db_file)
        self.table = db.table("scenarios", cache_size=cache_size)


if __name__ == '__main__':

    position_demonstration = Position("go_to_home", cartesian_coords=[1.5, 1.5, 1.5], root=True)


