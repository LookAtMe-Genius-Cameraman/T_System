#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: modelisation
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to Denavit-Hartenberg mathematical models of T_System's robotic arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import json
import numpy as np

from cloudpickle import dumps, loads
from numpy import linalg
from sympy import symbols, eye, Matrix, cos, sin, diff
from math import pi
from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher

from t_system import T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class ArmModeler:
    """Class to define the D-H matrix modeler of T_System arm .

        This class provides necessary initiations and a function named :func:`t_system.motion.arm.ArmModeler.create`
        for the create D-H model of the given arm.

    """

    def __init__(self):
        """Initialization method of :class:`t_system.motion.arm.modelisation.ArmModeler` class.
        """
        self.name = None

        self.config_file = f'{T_SYSTEM_PATH}/motion/arm/config.json'

        self.db = DBFetcher(f'{T_SYSTEM_PATH}/motion/arm', "model").fetch()

        self.joint_count = 0
        self.alpha = None
        self.a = None
        self.q = None
        self.d = None
        self.dh_params = {}
        self.tf_matrices = []

        self.jacobian_matrix = None

    def create(self, arm_name):
        """Method to create D-H model of given arm.

        Args:
            arm_name (str):                     A robotic arm name in to the config.json file.
        """
        try:
            with open(self.config_file) as conf_file:
                arm_configs = json.load(conf_file)[arm_name]  # config file returns the arms.
        except KeyError:
            raise Exception(f'{arm_name} is not exit in configuration file.')

        joint_configs = arm_configs["joints"]

        self.joint_count = len(joint_configs)

        self.__prepare_dh_params()
        self.__set_dh_params(joint_configs)

        self.__calc_jacobian_matrix()

        self.__db_upsert(force_insert=True)

    def get(self, arm_name=None):
        """Method to create D-H model of given arm.

        Args:
            arm_name (str):                     A robotic arm name in to the config.json file.
        """
        if arm_name:
            model = self.db.search((Query().name == arm_name))

            if model:
                return {"alpha": loads(model[0]["alpha"].encode("raw_unicode_escape")),
                        "a": loads(model[0]["a"].encode("raw_unicode_escape")),
                        "q": loads(model[0]["q"].encode("raw_unicode_escape")),
                        "d": loads(model[0]["d"].encode("raw_unicode_escape")),
                        "dh_params": loads(model[0]["dh_params"].encode("raw_unicode_escape")),
                        "transform_matrices": loads(model[0]["transform_matrices"].encode("raw_unicode_escape")),
                        "jacobian_matrix": loads(model[0]["jacobian_matrix"].encode("raw_unicode_escape"))}
            return None
        else:
            arms = []
            for model in self.db.all():
                arms.append({"alpha": loads(model[0]["alpha"].encode("raw_unicode_escape")),
                             "a": loads(model[0]["a"].encode("raw_unicode_escape")),
                             "q": loads(model[0]["q"].encode("raw_unicode_escape")),
                             "d": loads(model[0]["d"].encode("raw_unicode_escape")),
                             "dh_params": loads(model[0]["dh_params"].encode("raw_unicode_escape")),
                             "transform_matrices": loads(model[0]["transform_matrices"].encode("raw_unicode_escape")),
                             "jacobian_matrix": loads(model[0]["jacobian_matrix"].encode("raw_unicode_escape"))})
            return arms

    def show(self, arm_name=None):
        """Method to show model by given name parameter. If there is no name, print all arms models to the screen.

        Args:
            arm_name (str):                     A robotic arm name in to the config.json file.
        """

        if arm_name:
            model = self.get(arm_name)
            if model:
                for key, value in model.items():
                    print(f'{key}: \n{value}')
                return True

            logger.error(f'There is no model for arm {arm_name}')
            return False
        else:
            models = self.get()
            if models:
                for model in models:
                    for key, value in model.items():
                        print(f'{key}: \n{value}')
                return True

            logger.error(f'There is no any created model.')
            return False

    def __prepare_dh_params(self):
        """Method to preparing D-H parameters of Arm.
        """
        self.alpha = symbols('alpha0:' + str(self.joint_count))
        self.a = symbols('a0:' + str(self.joint_count))
        self.q = symbols('q1:' + str(self.joint_count + 1))
        self.d = symbols('d1:' + str(self.joint_count + 1))

    def __set_dh_params(self, joints):
        """Method to setting joint's D-H parameters.

        Args:
            joints (list):    The arm's joints list for preparing parameters of Denavit-Hartenberg chart.
        """
        self.dh_params = {}

        for i in range(len(joints)):
            self.dh_params[self.alpha[i]] = joints[i]["alpha"]

            self.dh_params[self.a[i]] = joints[i]["a"]

            if joints[i]["structure"] == "revolute":
                self.dh_params[self.q[i]] = self.q[i]
                self.dh_params[self.d[i]] = joints[i]["init_d"]

            elif joints[i]["structure"] == "prismatic":
                self.dh_params[self.q[i]] = joints[i]["init_q"]
                self.dh_params[self.d[i]] = self.d[i]

            elif joints[i]["structure"] == "constant":
                self.dh_params[self.q[i]] = joints[i]["init_q"]
                self.dh_params[self.d[i]] = joints[i]["init_d"]

        self.__set_transform_matrices()

    def show_dh_params(self):
        """Method to getting D-H parameters of joints of Arm as string message.
        """
        print(f'DH Parameters are: {self.dh_params}')

    def __set_transform_matrices(self):
        """Method to setting D-H transform matrices.
        """
        self.tf_matrices = []

        transform_matrix = eye(4)  # creates a unit matrix via passing argument.
        for i in range(self.joint_count):
            transform_matrix = transform_matrix * self.__create_tf_matrix(self.alpha[i], self.a[i], self.d[i], self.q[i]).subs(self.dh_params)
            self.tf_matrices.append(transform_matrix)

    def show_transform_matrices(self):
        """Method to getting D-H parameters of joints of Arm as string message.
        """

        print(f'Transform Matrices are: {self.tf_matrices}')

    @staticmethod
    def __create_tf_matrix(alpha, a, d, q):
        """Method to calculate transform matrix of Denavit-Hartenberg Method.

        Args:
            alpha:                      The twist angle. Axis angle between consecutive two axes.
            a:                          The limb length between consecutive two axis.
            d:                          link offset. The displacement along the same axis.
            q:                          The rotation theta angle about the joint axis.

        Returns:
            object:                     The Denavit-Hartenberg transform matrix object.
        """

        tf_matrix = Matrix([[cos(q), -sin(q), 0., a],
                            [sin(q) * cos(alpha), cos(q) * cos(alpha), -sin(alpha), -sin(alpha) * d],
                            [sin(q) * sin(alpha), cos(q) * sin(alpha), cos(alpha), cos(alpha) * d],
                            [0., 0., 0., 1.]])
        return tf_matrix

    def __calc_jacobian_matrix(self):
        """Method to calculate jacobian matrix of Arm's General Denavit-Hartenberg Transform Matrix.
        """

        tf_matrix_first_to_last = self.tf_matrices[-1]
        self.jacobian_matrix = [diff(tf_matrix_first_to_last[:3, -1], self.q[i]).reshape(1, 3) for i in range(len(self.q))]
        self.jacobian_matrix = Matrix(self.jacobian_matrix).T  # .T returns the transpose of matrix.

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):        Force insert flag.

        Returns:
            str:  Response.
        """

        if self.db.search((Query().name == self.name)):
            if force_insert:
                self.db.update({
                    'name': self.name,
                    'alpha': dumps(self.alpha).decode("raw_unicode_escape"),
                    'a': dumps(self.a).decode("raw_unicode_escape"),
                    'q': dumps(self.q).decode("raw_unicode_escape"),
                    'd': dumps(self.d).decode("raw_unicode_escape"),
                    'dh_params': dumps(self.dh_params).decode("raw_unicode_escape"),
                    'transform_matrices': dumps(self.tf_matrices).decode("raw_unicode_escape"),
                    'jacobian_matrix': dumps(self.jacobian_matrix).decode("raw_unicode_escape")
                }, Query().name == self.name)
            else:
                return "Already Exist"
        else:
            self.db.insert({
                'name': self.name,
                'alpha': dumps(self.alpha).decode("raw_unicode_escape"),
                'a': dumps(self.a).decode("raw_unicode_escape"),
                'q': dumps(self.q).decode("raw_unicode_escape"),
                'd': dumps(self.d).decode("raw_unicode_escape"),
                'dh_params': dumps(self.dh_params).decode("raw_unicode_escape"),
                'transform_matrices': dumps(self.tf_matrices).decode("raw_unicode_escape"),
                'jacobian_matrix': dumps(self.jacobian_matrix).decode("raw_unicode_escape")
            })  # insert the given data

        return ""
