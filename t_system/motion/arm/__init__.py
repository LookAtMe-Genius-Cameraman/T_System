#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: arm
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's motion ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import numpy as np
import json

from numpy import linalg
from sympy import symbols, eye, Matrix, cos, sin, diff
from math import pi
# from multipledispatch import dispatch

from t_system.motion.motor import ServoMotor
from t_system.motion import degree_to_radian
from t_system import T_SYSTEM_PATH


class Joint:
    """Class to define the joint of N-axis motion arm.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, joint):
        """Initialization method of :class:`t_system.motion.arm.Joint` class.

        Args:
            joint (dict):          The requested_data that is contain joint's properties from the config file.
        """
        self.number = joint['joint_number']

        self.motor = ServoMotor(joint['motor_gpio_pin'])

        self.structure = joint['structure']
        self.rotation_type = joint['rotation_type']

        if self.structure == 'revolute':
            self.max_q = joint['max_q']
            self.min_q = joint['min_q']

        elif self.structure == 'prismatic':
            self.max_d = joint['max_d']
            self.min_d = joint['min_d']

        self.d = joint['init_d']
        self.q = joint['init_q']
        self.a = joint['a']
        self.alpha = joint['alpha']

        self.current_angle = self.q

        self.motor.start(degree_to_radian(self.q))

    def move_to_angle(self, target_angle):
        """The top-level method to provide servo motors moving.

        Args:
            target_angle:       	        The target angle of servo motors. In radian Unit.
        """

        self.motor.directly_goto_position(target_angle)
        self.current_angle = target_angle

    def change_angle_by(self, delta_angle, direction):
        """The top-level method to provide servo motors moving.

        Args:
            delta_angle (float):            Angle to rotate. In degree.
            direction (bool):               Rotate direction. True means CW, otherwise CCW.
        """

        self.move_to_angle(self.calc_target_angle(degree_to_radian(delta_angle), direction))

    def calc_target_angle(self, delta_angle, direction):
        """The low-level method to calculate target angle with the given variation angle value.

        Args:
            delta_angle (float):            Calculated theta angle for going to object position. In radian type.
            direction (bool):               Rotate direction. True means CW, otherwise CCW.
        """

        if direction:
            if self.current_angle - delta_angle < 0 or self.current_angle - delta_angle > pi:
                return self.current_angle
            return self.current_angle - delta_angle  # this mines (-) for cw.
        else:
            if self.current_angle + delta_angle < 0 or self.current_angle + delta_angle > pi:
                return self.current_angle
            return self.current_angle + delta_angle


class Arm:
    """Class to define a N-axis arm for motion ability of tracking system.

        This class provides necessary initiations and a function named :func:`t_system.motor.Motor.move`
        for the provide move of servo motor.

    """

    def __init__(self, arm_name="Junior"):
        """Initialization method of :class:`t_system.motion.arm.Arm` class.

        Args:
            arm_name (str):         Name of the arm. From config file or user choice.
        """
        self.name = arm_name
        self.joints = []

        self.joint_count = 0
        self.alpha = None
        self.a = None
        self.q = None
        self.d = None
        self.dh_params = {}
        self.tf_matrices_list = []

        self.jacobian_matrix = None

        self.current_pos_as_coord = []
        self.current_pos_as_theta = []

        with open(f'{T_SYSTEM_PATH}/motion/arm/arm_config.json') as conf_file:
            joints = json.load(conf_file)[arm_name]  # config file returns the arms.

        self.set_joints(joints)
        self.set_dh_params(self.joints)

    def set_joints(self, joints):
        """The high-level method to setting joints with D-H parameters.

        Args:
            joints (list):          The joint list from the config file.
        """
        self.joint_count = len(joints)
        for joint in joints:
            self.joints.append(Joint(joint))

        self.prepare_dh_params()

    def prepare_dh_params(self):
        """The high-level method to preparing D-H parameters of Arm.
        """
        self.alpha = symbols('alpha0:' + str(self.joint_count))
        self.a = symbols('a0:' + str(self.joint_count))
        self.q = symbols('q1:' + str(self.joint_count + 1))
        self.d = symbols('d1:' + str(self.joint_count + 1))

    def set_dh_params(self, joints):
        """The high-level method to setting joint's D-H parameters.

        Args:
            joints (list):    The arm's joints list for preparing parameters of Denavit-Hartenberg chart.
        """
        for i in range(len(joints)):
            self.dh_params[self.alpha[i]] = joints[i].alpha

            self.dh_params[self.a[i]] = joints[i].a

            if joints[i].structure == 'revolute':
                self.dh_params[self.q[i]] = self.q[i]
                self.dh_params[self.d[i]] = joints[i].d

            elif joints[i].structure == 'prismatic':
                self.dh_params[self.q[i]] = joints[i].q
                self.dh_params[self.d[i]] = self.d[i]

        self.set_tranform_matrices()

    def show_dh_params(self):
        """The high-level method to getting D-H parameters of joints of Arm as string message.
        """
        print('DH Parameters are: {}'.format(self.dh_params))

    def set_tranform_matrices(self):
        """The low-level method to setting D-H transform matrices.
        """

        transform_matrix = eye(4)  # creates a unit matrix via passing argument.
        for i in range(self.joint_count):
            transform_matrix = transform_matrix * self.create_tf_matrix(self.alpha[i], self.a[i], self.d[i], self.q[i]).subs(self.dh_params)
            self.tf_matrices_list.append(transform_matrix)

    def show_transform_matrices(self):
        """The high-level method to getting D-H parameters of joints of Arm as string message.
        """

        print('Transform Matrices are: {}'.format(self.tf_matrices_list))

    @staticmethod
    def create_tf_matrix(alpha, a, d, q):
        """The high-level method to calculate transform matrix of Denavit-Hartenberg Method.

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

    def forward_kinematics(self, theta_list):
        """The high-level method to calculate forword kinematics of the Arm.

        Args:
            theta_list (list):          The list of current joints angles.

        Returns:
            list:                       The cartesian coordinate position of Arm's farthest point as theta list.
        """

        to_current_pos = []
        theta_dict = {}
        tf_matrix_first_to_last = self.tf_matrices_list[-1]

        for i in range(len(theta_list)):
            theta_dict[self.q[i]] = theta_list[i]

        temp = tf_matrix_first_to_last.evalf(subs=theta_dict, chop=True, maxn=4)

        x = [np.array(temp[0, -1]).astype(np.float64)]
        y = [np.array(temp[1, -1]).astype(np.float64)]
        z = [np.array(temp[2, -1]).astype(np.float64)]

        to_current_pos.append(np.array([x, y, z]))

        return to_current_pos

    def calc_jacobian_matrix(self):
        """The low-level method to calculate jacobian matrix of Arm's General Denavit-Hartenberg Transform Matrix.
        """

        tf_matrix_first_to_last = self.tf_matrices_list[-1]
        self.jacobian_matrix = [diff(tf_matrix_first_to_last[:3, -1], self.q[i]).reshape(1, 3) for i in range(len(self.q))]
        self.jacobian_matrix = Matrix(self.jacobian_matrix).T  # .T returns the transpose of matrix.

    def inverse_kinematics(self, guess, target_point):
        """The high-level method to calculate forword kinematics of the Arm.

        Args:
            guess:                      The twist angle. Axis angle between consecutive two axes.
            target_point (list):              Target point's coordinates as X, Y, Z respectively.

        Returns:
            list:                       The angular position list of joints by the target point. (unit: radian)
        """

        error = 1.0
        tolerance = 0.05

        # Initial Guess - Joint Angles
        thetas = guess  # thetas is list which is contain all axes theta angles.
        target_point = np.matrix(target_point)  # X, Y, Z list to matrix for Target Position
        # print(target_point.shape)
        # Jacobian
        self.calc_jacobian_matrix()
        tf_matrix_first_to_last = self.tf_matrices_list[-1]

        error_grad = []

        theta_dict = {}

        lr = 0.2
        while error > tolerance:
            for i in range(len(thetas)):
                theta_dict[self.q[i]] = thetas[i]

            calculated_target_point = np.matrix(self.forward_kinematics(thetas)[-1])

            diff_wanted_calculated = target_point - calculated_target_point

            thetas = thetas + lr * (np.matrix(self.jacobian_matrix.evalf(subs=theta_dict, chop=True, maxn=4)).astype(np.float64).T * diff_wanted_calculated).T
            thetas = np.array(thetas)[0]  # this line's purpose is changing Q from matrix level to array level.

            prev_error = error

            error = linalg.norm(diff_wanted_calculated)

            if error > 10 * tolerance:
                lr = 0.3
            elif error < 10 * tolerance:
                lr = 0.2
            error_grad.append((error - prev_error))

        # print(error)
        return thetas

    def path_plan(self, guess, target_list, time, acceleration):
        Q_list = []
        for target in target_list:
            Q = self.inverse_kinematics(guess, target)
            predicted_coordinates = self.forward_kinematics(Q)[-1]
            print('Target: {} ,  Predicted: {}'.format(target, predicted_coordinates))
            Q_list.append(Q)
            guess = Q
        # print(np.matrix(Q_list), np.matrix(Q_list).shape)
        Q_matrix = np.matrix(Q_list)
        theta_all, omega_all, acceleration_all = lpsb.trajectory_planner(Q_matrix, time, acceleration, 0.01)
        return Q_list

    def goto_position(self, pos_thetas=None, pos_coords=None):
        """The high-level method to go to given position via position angles or coordinates of the Arm.

           If the target position is given with angles, cartesian coordinates have been created,
           else cartesian coordinates given the joints angles create.

        Args:
            pos_thetas (list):          Angular position list to go. List length equals to joint count.
            pos_coords (list):          Cartesian position list to go. List length equals to 3 for 3 dimensions of the cartesian coordinate system.

        """

        if pos_coords and pos_thetas:
            self.rotate_joints(pos_thetas)

        elif pos_thetas:
            self.rotate_joints(pos_thetas)

            pos_coords = self.forward_kinematics(pos_thetas)[-1]

        elif pos_coords:
            pos_thetas = self.inverse_kinematics(self.current_pos_as_theta, pos_coords)

            self.rotate_joints(pos_thetas)

        else:
            raise Exception('Going to position requires angle or coordinate!')

        self.current_pos_as_theta = pos_thetas
        self.current_pos_as_coord = pos_coords

    def rotate_joints(self, pos_thetas):
        """The low-level method to rotate all joints according to given position theta angles.

        Args:
            pos_thetas (list):          Angular position list to go. List length equals to joint count.
        """

        for joint in self.joints:
            joint.move_to_angle(pos_thetas[joint.number - 1])

    def rotate_single_joint(self, joint_number, delta_angle, direction=None):
        """The high-level method to move a single joint towards the given direction with the given variation.

        Args:
            joint_number (int):        Number of one of arm's joints.
            delta_angle (float):       Angle to rotate.
            direction (bool):          Rotate direction. True means CW, otherwise CCW.
        """
        print("in here")
        if direction is None:
            direction = False
            if delta_angle <= 0:
                direction = True

            delta_angle = abs(delta_angle)

        for joint in self.joints:
            if joint.number == joint_number:
                joint.change_angle_by(delta_angle, direction)

    def move_endpoint(self, axis, distance):
        """The high-level method to move endpoint of the arm with the given axis and the distance.

        Args:
            axis (str):                Number of one of arm's joints.
            distance (int):            Moving distance.
        """

        current_pos_as_coord = self.current_pos_as_coord
        cartesian_coords = {"x": current_pos_as_coord[0], "y": current_pos_as_coord[1], "z": current_pos_as_coord[2]}

        cartesian_coords[axis] += distance

        self.goto_position(pos_coords=current_pos_as_coord)

    def ang_diff(self, theta1, theta2):
        """
        Returns the difference between two angles in the range -pi to +pi
        """

        return (theta1 - theta2 + np.pi) % (2 * np.pi) - np.pi


