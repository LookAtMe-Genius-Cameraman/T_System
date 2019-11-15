#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: action
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to setting predicted positions and creating scenarios ability for T_System's robotic arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import uuid  # The random id generator
import time  # Time access and conversions

from multipledispatch import dispatch
from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher

from t_system import dot_t_system_dir, T_SYSTEM_PATH

from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class MissionManager:
    """Class to define a mission manager to managing movements of Arm and Locking System(when it is using independent from seer during tracking non-moving objects) during job.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.MissionManager.execute`
        for the realize mission that is formed positions or scenarios.

    """

    def __init__(self):
        """Initialization method of :class:`t_system.motion.action.ActionManager` class.
        """

        db_folder = f'{T_SYSTEM_PATH}/motion/action'
        self.predicted_db_name = 'predicted_missions'
        self.predicted_scenarios_table = DBFetcher(db_folder, self.predicted_db_name, "scenarios", 30).fetch()
        self.predicted_positions_table = DBFetcher(db_folder, self.predicted_db_name, "positions", 30).fetch()

        db_folder = dot_t_system_dir
        self.db_name = 'missions'
        self.scenarios_table = DBFetcher(db_folder, self.db_name, "scenarios").fetch()
        self.positions_table = DBFetcher(db_folder, self.db_name, "positions").fetch()

        self.predicted_positions = []
        self.predicted_scenarios = []
        self.positions = []
        self.scenarios = []

        self.refresh_members()

        self.actor = Actor()

    def refresh_members(self):
        """Method to refreshing the members
        """
        self.predicted_scenarios = []
        self.predicted_positions = []
        self.scenarios = []
        self.positions = []

        predicted_scenarios = self.predicted_scenarios_table.all()
        for scenario in predicted_scenarios:
            self.predicted_scenarios.append(Scenario(scenario["name"], scenario["id"], root=True, db_name=self.predicted_db_name))

        predicted_positions = self.predicted_positions_table.all()
        for position in predicted_positions:
            self.predicted_positions.append(Position(position["name"], position["id"], position["cartesian_coords"], position["polar_params"], root=True, db_name=self.predicted_db_name))

        scenarios = self.scenarios_table.all()
        for scenario in scenarios:
            self.scenarios.append(Scenario(scenario["name"], scenario["id"], root=False, db_name=self.db_name))

        positions = self.positions_table.all()
        for position in positions:
            self.positions.append(Position(position["name"], position["id"], position["cartesian_coords"], position["polar_params"], root=False, db_name=self.db_name))

    def continuous_execute(self, stop, pause, mission, m_type, root):
        """The top-level method for executing the missions as continuously.

        Args:
            stop:       	                Stop flag of the tread about terminating it outside of the function's loop.
            pause:       	                Pause flag of the tread about freezing it outside of the function's loop.
            mission (str):                  Name of the position or scenario that is created for mission.
            m_type (str):                   Type of the mission. Either `position` or `scenario`.
            root (bool):                    Root privileges flag.
        """

        while True:
            self.execute(mission, m_type, root)
            if stop():
                break

    def execute(self, mission, m_type, root):
        """The top-level method to fulfill mission with using position or scenarios their names specified with given parameter.

        Args:
            mission (str):                  Name of the position or scenario that is created for mission.
            m_type (str):                   Type of the mission. Either `position` or `scenario`.
            root (bool):                    Root privileges flag.
        """
        result = False

        if root:
            positions = self.predicted_positions
            scenarios = self.predicted_scenarios
        else:
            positions = self.positions
            scenarios = self.scenarios

        if m_type == "position":
            for position in positions:
                if position.name == mission:
                    self.actor.act(position)
                    result = True
                    break

        elif m_type == "scenario":
            for scenario in scenarios:
                if scenario.name == mission:
                    self.actor.act([scenario])
                    result = True
                    break

        return result

    def expand_actor(self):
        """Method to expand actor with using axes and motors of target_locker of t_system's vision.
        """
        from t_system import seer
        expansion_angles = seer.reload_target_locker(arm_expansion=True)
        self.actor.expand(current_angles=expansion_angles)

    def revert_the_expand_actor(self):
        """Method to revert back the expansion.
        """

        from t_system import seer

        locker_angles = self.actor.revert_the_expand()  # locker angles respectively are pan and tilt

        seer.reload_target_locker(arm_expansion=False, current_angles=locker_angles)


class EmotionManager:
    """Class to define emotion manager to managing movements of Arm and Locking System(when it is using independent from seer during tracking non-moving objects) for creating emotion effects.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.EmotionManager.make_feel`
        for the realize emotion that is formed positions or scenarios.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.motion.action.EmotionManager` class.
        """

        db_folder = f'{T_SYSTEM_PATH}/motion/action'
        self.db_name = 'emotions'
        self.scenarios_table = DBFetcher(db_folder, self.db_name, "scenarios", 30).fetch()
        self.positions_table = DBFetcher(db_folder, self.db_name, "positions", 30).fetch()

        self.positions = []
        self.scenarios = []

        self.refresh_members()

        self.actor = Actor()

    def refresh_members(self):
        """Method to refreshing the members
        """
        self.scenarios = []
        self.positions = []

        scenarios = self.scenarios_table.all()
        for scenario in scenarios:
            self.scenarios.append(Scenario(scenario["name"], scenario["id"], root=True, db_name=self.db_name))

        positions = self.positions_table.all()
        for position in positions:
            self.positions.append(Position(position["name"], position["id"], position["cartesian_coords"], position["polar_params"], root=True, db_name=self.db_name))

    def make_feel(self, emotion, e_type):
        """The top-level method to generating emotion with using position or scenarios their names specified with given parameter.

        Args:
            emotion (str):                  Name of the position or scenario that is created for emotion.
            e_type (str):                   Type of the emotion. Either `position` or `scenario`.
        """
        self.expand()

        if e_type == "position":
            for position in self.positions:
                if position.name == emotion:
                    self.actor.act(position)
                    break

        elif e_type == "scenario":
            for scenario in self.scenarios:
                if scenario.name == emotion:
                    self.actor.act([scenario])
                    break

    def expand(self):
        """Method to expand actor with using axes and motors of target_locker of t_system's vision.
        """
        from t_system import seer
        expansion_angles = seer.reload_target_locker(arm_expansion=True)

        self.actor.expand(current_angles=expansion_angles)

    def revert_the_expand_actor(self):
        """Method to revert back the expansion.
        """
        from t_system import seer

        locker_angles = self.actor.revert_the_expand()  # locker angles respectively are pan and tilt

        seer.reload_target_locker(arm_expansion=False, current_angles=locker_angles)


class Actor:
    """Class to define an actor to fulfill tasks with given positions and scenarios.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Actor.`
        for the provide move of servo motor.

    """

    def __init__(self):
        """Initialization method of :class:`t_system.motion.action.Actor` class.
        """
        from t_system import arm

        self.arm = arm

    @dispatch(object)
    def act(self, position):
        """Method to acting by given position object.

        Args:
            position (Position):            A Position object
        """

        self.arm.goto_position(polar_params={"coords": position.polar_coords,
                                             "delays": position.polar_delays,
                                             "divide_counts": position.polar_divide_counts}, cartesian_coords=position.cartesian_coords)

    @dispatch(list)
    def act(self, scenarios):
        """Method to acting by given scenarios object.

        Args:
            scenarios (list):               Scenario object list
        """

        for scenario in scenarios:
            for position in scenario.positions:
                self.arm.goto_position(polar_params={"coords": position.polar_coords,
                                                     "delays": position.polar_delays,
                                                     "divide_counts": position.polar_divide_counts}, cartesian_coords=position.cartesian_coords)

    def expand(self, current_angles=None):
        """Method to expand arm with using axes and motors of target_locker of t_system's vision.

        Args:
            current_angles (list):          Current angles of the arm's expanded joints.
        """

        self.arm.expand(current_angles=current_angles)

    def revert_the_expand(self):
        """Method to revert back the expansion.
        """

        return self.arm.revert_the_expand()


class Scenario:
    """Class to define scenarios via creating path with given positions.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Scenario.add_positions`
        for the provide entry point to adding new positions to the scenario.

    """

    def __init__(self, name, id=None, root=False, db_name="predicted_missions"):
        """Initialization method of :class:`t_system.motion.action.Scenario` class.

        Args:
            id (str):                       The id of the scenario.
            name (str):                     The name of the scenario.
            root (bool):                    Root privileges flag.
            db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        self.positions = []
        self.root = root
        self.db_name = db_name

        if self.root:
            db_folder = f'{T_SYSTEM_PATH}/motion/action'
            self.table = self.__get_db(db_folder, db_name, 30)
        else:
            db_folder = dot_t_system_dir
            db_name = 'missions'
            self.table = self.__get_db(db_folder, db_name)

        self.__refresh_positions()

    def update_all_positions(self, positions):
        """Method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """
        self.positions.clear()
        self.positions.extend(positions)
        self.db_upsert(force_insert=True)

    def add_positions(self, positions):
        """Method to add position to the scenario.

        Args:
            positions (list):               Position object list.
        """

        self.positions.extend(positions)
        self.db_upsert(force_insert=True)

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
                self.table.update({
                    'name': self.name,
                    'positions': [{
                        "id": position.id,
                        "name": position.name,
                        "cartesian_coords": position.cartesian_coords,
                        "polar_params": {
                            "coords": position.polar_coords,
                            "delays": position.polar_delays,
                            "divide_counts": position.polar_divide_counts
                        }
                    } for position in self.positions]}, Query().id == self.id)
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
                    "polar_params": {
                        "coords": position.polar_coords,
                        "delays": position.polar_delays,
                        "divide_counts": position.polar_divide_counts
                    }
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

    def __refresh_positions(self):
        """Method to refreshing the members
        """

        scenario = self.table.search((Query().id == self.id))
        if scenario:
            for position in scenario[0]["positions"]:
                self.positions.append(Position(position["name"], position["id"], position["cartesian_coords"], position["polar_params"], self.root, self.db_name, is_for_scenario=True))


class Position:
    """Class to define the position of the arm with cartesian coordinates of arms' last point and angle value of its joints.

        This class provides necessary initiations and a function named :func:`t_system.motion.action.Position.update_coords`
        for updating utilities of itself.

    """

    def __init__(self, name, id=None, cartesian_coords=None, polar_params=None, root=False, db_name="predicted_missions", is_for_scenario=False):
        """Initialization method of :class:`t_system.motion.arm.action.Position` class.

        Args:
            name (str):                     The name of the position.
            id (str):                       The id of the position.
            cartesian_coords (list):        Cartesian coordinate value list of the position.
            polar_params (dict):            Dict of polar coordinate, delay and step value list of the position.
            root (bool):                    Root privileges flag.
            db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
            is_for_scenario (bool):         Flag that is specified position is inside a scenario.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.name = name
        self.cartesian_coords = cartesian_coords

        self.polar_coords = None
        self.polar_delays = None
        self.polar_divide_counts = None
        if polar_params:
            self.polar_coords = polar_params["coords"]
            self.polar_delays = polar_params["delays"]
            self.polar_divide_counts = polar_params["divide_counts"]

        self.root = root
        self.is_for_scenario = is_for_scenario

        if self.root:
            db_folder = f'{T_SYSTEM_PATH}/motion/action'
            self.table = self.__get_db(db_folder, db_name, 30)
        else:
            db_folder = dot_t_system_dir
            db_name = 'missions'
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
                    self.table.update({'name': self.name, 'cartesian_coords': self.cartesian_coords, 'polar_params': {'coords': self.polar_coords, 'delays': self.polar_delays, 'divide_counts': self.polar_divide_counts}}, Query().id == self.id)

                else:
                    return "Already Exist"
            else:
                self.table.insert({
                    'id': self.id,
                    'name': self.name,
                    'cartesian_coords': self.cartesian_coords,
                    'polar_params': {'coords': self.polar_coords, 'delays': self.polar_delays, 'divide_counts': self.polar_divide_counts}
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
