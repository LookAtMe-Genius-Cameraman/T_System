#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: accession
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's accessing external network and creating internal network(becoming access point) ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import os  # Miscellaneous operating system interfaces
import datetime  # Basic date and time types
import subprocess  # Subprocess managements

from PyAccessPoint import pyaccesspoint
from wifi import Cell, Scheme
from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database

from t_system import dot_t_system_dir


class AccessPoint:
    """Class to define a becoming access point ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.accession.AccessPoint.set_set_parameters`
    as the external setting point of the access point utilities.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.accession.AccessPoint` class.

        Args:
            args:                   Command-line arguments.
        """

        self.wlan = args["wlan"]
        self.inet = args["inet"]
        self.ip = args["ip"]
        self.netmask = args["netmask"]
        self.ssid = args["ssid"]
        self.password = args["password"]

        self.access_point = None

    def set_parameters(self, wlan=None, inet=None, ip=None, netmask=None, ssid=None, password=None):
        """The high-level method to set access point parameters.

        Args:
            wlan:       	        wi-fi interface that will be used to create hotSpot
            inet:       	        forwarding interface
            ip:       	            ip address of this machine in new network
            netmask:       	        Netmask address.
            ssid:       	        Preferred access point name.
            password:       	    Password of the access point.
        """

        if wlan:
            self.wlan = wlan
        if inet:
            self.inet = inet
        if ip:
            self.ip = ip
        if netmask:
            self.netmask = netmask
        if ssid:
            self.ssid = ssid
        if password:
            self.password = password

        self.access_point = pyaccesspoint.AccessPoint(wlan=self.wlan, inet=self.inet, ip=self.ip, netmask=self.netmask, ssid=self.ssid, password=self.password)

    def start(self):
        """The high-level method to start serving network connection.
        """

        self.access_point.start()

    def stop(self):
        """The high-level method to stop serving network connection.
        """

        self.access_point.stop()

    def check_status(self):
        """The high-level method to sending access point's working status.
        """

        return self.access_point.is_running()


class NetworkManager:
    """Class to define an accessing to the around networks ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.audition.Audition.listen_async`
    as the loop for asynchronous collecting audio data to the vision ability, named :func:`t_system.audition.Audition.listen_sync`
    for the synchronous collecting audio data to the vision ability and named :func:`t_system.audition.Audition.start_recording`
    as entry point from vision ability for starting recording processes.
    """

    def __init__(self, wlan="wlp4s0"):
        """Initialization method of :class:`t_system.accession.NetworkManager` class.

        Args:
            args:                   Command-line arguments.
            wlan:       	        wi-fi interface that will be used to create hotSpot.
        """

        self.folder = dot_t_system_dir + "/network"
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        self.db = TinyDB(self.folder + '/db.json')

        self.wlan = wlan

        self.cells = []
        self.available_networks = []

    def scan(self, wlan="wlp4s0"):
        """The high-level method to scan around for searching available networks.

        Args:
            wlan:       	        wi-fi interface that will be used to create hotSpot.
        """

        self.wlan = wlan
        self.cells = list(Cell.all(self.wlan))

    def set_available_networks(self):
        """The low-level method to setting available networks with their ssid and passwords.
        """
        self.available_networks.clear()

        for cell in self.cells:
            network = {"ssid": cell.ssid, "password": ""}
            self.available_networks.append(network)

    def set_network(self, ssid, password):
        """The high-level method to set network parameter for reaching it.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
        """

        status = False

        for network in self.available_networks:
            if ssid == network["ssid"]:
                network["password"] = password
                status = True

        return status

    def connect(self, ssid, password):
        """The high-level method to try connect to one of available networks.
        """
        for cell in self.cells:
            if cell.ssid == ssid:
                scheme = Scheme.for_cell(self.wlan, ssid, cell, password)
                scheme.activate()

