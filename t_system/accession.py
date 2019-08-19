#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: accession
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's accessing external network and creating internal network(becoming access point) ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time  # Time access and conversions
import os  # Miscellaneous operating system interfaces
import requests

from PyAccessPoint import pyaccesspoint
from wifi import Cell, Scheme
from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from subprocess import call, check_output # Subprocess managements
from multipledispatch import dispatch
from elevate import elevate  # partial root authentication interface

from t_system.administration import check_secret_root_entry
from t_system.db_fetching import DBFetcher
from t_system import dot_t_system_dir


def set_local_ip_address(wlan, ip_address):
    """The high-level method to set static local ip address.

    Args:
        wlan (str):       	        wi-fi interface that will be used to connect to external network
        ip_address (str):           Static ip address of this machine the network
    """
    from pyroute2 import IPRoute, NetlinkError
    ip = IPRoute()
    index = ip.link_lookup(ifname=wlan)[0]
    try:
        ip.addr('add', index, address=ip_address, mask=24)

    except NetlinkError as e:
        print(e)

    ip.close()


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

        self.wlan = args["ap_wlan"]
        self.inet = args["ap_inet"]
        self.ip = args["ap_ip"]
        self.netmask = args["ap_netmask"]
        self.ssid = args["ssid"]
        self.password = args["password"]

        self.access_point = pyaccesspoint.AccessPoint(wlan=self.wlan, inet=self.inet, ip=self.ip, netmask=self.netmask, ssid=self.ssid, password=self.password)

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

        if self.is_working():
            self.stop()
        else:
            pass
        self.access_point.start()
        print("AP started")

    def stop(self):
        """The high-level method to stop serving network connection.
        """

        self.access_point.stop()

    def is_working(self):
        """The high-level method to sending access point's working status.
        """

        return self.access_point.is_running()


class NetworkConnector:
    """Class to define an accessing to the around networks ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.audition.Audition.listen_async`
    as the loop for asynchronous collecting audio data to the vision ability, named :func:`t_system.audition.Audition.listen_sync`
    for the synchronous collecting audio data to the vision ability and named :func:`t_system.audition.Audition.start_recording`
    as entry point from vision ability for starting recording processes.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.accession.NetworkManager` class.

        Args:
            args:                   Command-line arguments.
        """

        self.folder = dot_t_system_dir + "/network"
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        self.table = DBFetcher(self.folder, "db", "login").fetch()

        self.wpa_supplicant = WpaSupplicant(args)

        self.wlan = args["wlan"]

        self.current_cells = []
        self.current_available_networks = []
        self.known_networks = []

        set_local_ip_address(args["wlan"], args["static_ip"])

        self.scan()
        self.set_available_networks()
        self.refresh_known_networks()

    def scan(self, wlan=None):
        """The high-level method to scan around for searching available networks.

        Args:
            wlan:       	        wi-fi interface that will be used to create hotSpot.
        """
        if wlan:
            self.wlan = wlan
        self.current_cells = list(Cell.all(self.wlan))

    def set_available_networks(self):
        """The low-level method to setting available networks with their ssid and passwords.
        """
        self.current_available_networks.clear()

        for cell in self.current_cells:
            network = {"ssid": cell.ssid}
            self.current_available_networks.append(network)

    def add_network(self, ssid, password):
        """The high-level method to set network parameter for reaching it.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
        """

        admin_id = check_secret_root_entry(ssid, password)
        if admin_id:
            return True, admin_id

        status = False

        for network in self.current_available_networks:
            if ssid == network["ssid"]:
                self.db_upsert(ssid, password)
                self.refresh_known_networks()
                status = True

        return status, admin_id

    def delete_network(self, ssid):
        """The high-level method to set network parameter for reaching it.

        Args:
            ssid:       	        The name of the surrounding access point.
        """

        self.table.remove((Query().ssid == ssid))

    @dispatch()
    def connect(self):
        """The high-level method to try to connect to one of the available networks using wpa_supplicant.conf file that is restarted by subprocess.
        """

        result = False
        self.wpa_supplicant.restart_ws_service()

        time.sleep(5)
        if self.is_network_online():
            print("Network connection established!")
            # result = True

        return result

    @dispatch(str, str)
    def connect(self, ssid, password):
        """The high-level method to try connect to one of available networks with using `wifi` library.

        Args:
            ssid (str):       	        The name of the surrounding access point.
            password (str):       	    The password of the surrounding access point.
        """
        result = False
        for cell in self.current_cells:
            if cell.ssid == ssid:
                try:
                    scheme = Scheme.for_cell(self.wlan, ssid, cell, password)
                    scheme.activate()
                    result = True
                except Exception as e:
                    print(e)

        return result

    def try_creating_connection(self):
        """The high-level method to try connect to one of available networks.
        """

        for network in self.known_networks:
            if self.connect(network["ssid"], network["password"]):
                return True
        return False

    def db_upsert(self, ssid, password, force_insert=False):
        """Function to insert(or update) the position to the database.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().ssid == ssid)):
            if force_insert:
                # self.already_exist = False
                self.table.update({'password': password, 'wlan': self.wlan}, Query().ssid == ssid)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'wlan': self.wlan,
                'ssid': ssid,
                'password': password
            })  # insert the given data

        return ""

    def refresh_known_networks(self):
        """The low-level method to refreshing known networks from the database (and creating objects for them.)
        """

        self.known_networks.clear()
        self.wpa_supplicant.create_wsc()

        for login in self.table.all():
            network = {"ssid": login["ssid"], "password": login["password"], "wlan": login["wlan"]}
            self.known_networks.append(network)
            self.wpa_supplicant.add_network_to_wsc(login["ssid"], login["password"])

    @staticmethod
    def is_network_online():
        """The top-level method to check the internet access of the current network connection via sending request to Google. 

        Returns:
            bool:  status.
        """
        
        url = 'http://www.google.com/'
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            # print("Internet connection could not be established.")
            pass
        return False


class WpaSupplicant:
    """Class to define a wpa supplicant handler to managing wpa_supplicant.conf file for its headers and networks.

    This class provides necessary initiations and functions named :func:`t_system.audition.Audition.listen_async`
    as the loop for asynchronous collecting audio data to the vision ability, named :func:`t_system.audition.Audition.listen_sync`
    for the synchronous collecting audio data to the vision ability and named :func:`t_system.audition.Audition.start_recording`
    as entry point from vision ability for starting recording processes.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.accession.NetworkManager` class.

        Args:
            args:                   Command-line arguments.
        """

        self.wpa_supp_conf_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
        self.country_code = args["country_code"]

        self.conf_headers = ["ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev", "update_config=1", f'country={self.country_code}']

        self.check_wsc()

    def check_wsc(self):
        """The high-level method to check wpa_supplicant.conf file's validation. If the file is not valid, method creates new valid file.
        """

        if os.path.isfile(self.wpa_supp_conf_file):
            elevate(show_console=False, graphical=False)

            wpa_supp_file = open(self.wpa_supp_conf_file, "r")
            correct_header_count = 0
            for line in wpa_supp_file:
                if self.conf_headers[0] in line:
                    correct_header_count += 1
                if self.conf_headers[1] in line:
                    correct_header_count += 1
                if self.conf_headers[2] in line:
                    correct_header_count += 1

            wpa_supp_file.close()

            if correct_header_count != 3:
                print("wpa_supplicant.conf is not valid. Creating new one.")
                self.create_wsc()

        else:
            self.create_wsc()

    @staticmethod
    def restart_ws_service():
        """The high-level method to restart wpa_supplicant service with reconfigured wpa_supplicant.conf file.
        """

        call("wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf", shell=True)

    def create_wsc(self):
        """The high(and low)-level method to create initialization wpa_supplicant.conf file.
        """

        print('Trying to create file wpa_supplicant.conf')
        time.sleep(0.5)

        f = open(self.wpa_supp_conf_file, "w")
        f.write(self.conf_headers[0] + '\n')
        f.write(self.conf_headers[1] + '\n')
        f.write(self.conf_headers[2] + '\n')
        f.close()

        os.system('sudo chown root:root ' + self.wpa_supp_conf_file)
        os.system('sudo chmod 600 ' + self.wpa_supp_conf_file)

        if os.path.isfile(self.wpa_supp_conf_file):
            print('File created successfully')

    def add_network_to_wsc(self, ssid, password, priority=None):
        """The high(and low)-level method to add new network ssid and psk information to wpa_supplicant.conf file.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
            priority (int):         The priority flag.
        """

        command_txt = f'sudo wpa_passphrase "{ssid}" "{password}"'

        result = check_output(command_txt, shell=True)

        f = open(self.wpa_supp_conf_file, 'a')
        for line in result:
            if priority is not None and "}" in line:
                f.write(f'\tpriority={priority}\n')
            f.write(line)
        f.close()




