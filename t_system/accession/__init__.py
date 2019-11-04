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
from wifi import Cell, Scheme, exceptions
from tinydb import Query  # TinyDB is a lightweight document oriented database
from subprocess import call, check_output # Subprocess managements
from multipledispatch import dispatch
from elevate import elevate  # partial root authentication interface

from t_system.db_fetching import DBFetcher
from t_system.administration import check_secret_root_entry

from t_system import dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def set_local_ip_address(wlan, ip_address):
    """Method to set static local ip address.

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
        logger.error(e)

    ip.close()


def restart_interface(interface):
    """Method to restart the network interface via subprocess.

    Args:
        interface:       	        wi-fi interface that will be used to create hotSpot.
    """

    call(['ifdown', interface])
    time.sleep(1)
    call(['ifup', interface])
    time.sleep(2)


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
        """Method to set access point parameters.

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
        """Method to start serving network connection.
        """

        if self.is_working():
            self.stop()
        else:
            pass
        self.access_point.start()

        logger.info("AP started")

    def stop(self):
        """Method to stop serving network connection.
        """

        self.access_point.stop()

    def is_working(self):
        """Method to sending access point's working status.
        """

        return self.access_point.is_running()


class NetworkConnector:
    """Class to define an accessing to the around networks ability of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.accession.NetworkConnector.connect`
    for the connecting with wpa_supplicant.conf or wifi.Scheme.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.accession.NetworkConnector` class.

        Args:
            args:                   Command-line arguments.
        """

        self.folder = f'{dot_t_system_dir}/network'
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        self.login_table = DBFetcher(self.folder, "db", "login").fetch()
        self.status_table = DBFetcher(self.folder, "db", "status").fetch()

        self.activity = None
        self.__refresh_status()

        self.wpa_supplicant = WpaSupplicant(args)

        self.wlan = args["wlan"]
        self.interface_ec = 0

        self.current_cells = []
        self.current_available_networks = []
        self.known_networks = []

        if args["static_ip"]:
            set_local_ip_address(args["wlan"], args["static_ip"])

        if self.activity:
            self.scan()
            self.__set_available_networks()

        self.__refresh_known_networks()

    def scan(self, wlan=None):
        """Method to scan around for searching available networks.

        Args:
            wlan:       	        wi-fi interface that will be used to create hotSpot.
        """

        if wlan:
            self.wlan = wlan

        try:
            self.current_cells = list(Cell.all(self.wlan))
        except exceptions.InterfaceError:

            if self.interface_ec < 1:
                logger.warning(f'InterfaceError for {self.interface_ec} times...')
                self.interface_ec += 1
                restart_interface(self.wlan)
                self.scan()

            else:
                logger.error(exceptions.InterfaceError(f'Error can not resolved!'))
                self.current_cells = []

    def __set_available_networks(self):
        """Method to setting available networks with their ssid and passwords.
        """
        self.current_available_networks.clear()

        for cell in self.current_cells:
            network = {"ssid": cell.ssid}
            self.current_available_networks.append(network)

    def add_network(self, ssid, password):
        """Method to set network parameter for reaching it.

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
                self.login_upsert(ssid, password)
                self.__refresh_known_networks()
                self.wpa_supplicant.add_network_to_wsc(ssid, password)
                self.__restart_networking_service()
                status = True
                break

        return status, admin_id

    def delete_network(self, ssid):
        """Method to set network parameter for reaching it.

        Args:
            ssid:       	        The name of the surrounding access point.
        """

        self.login_table.remove((Query().ssid == ssid))
        self.wpa_supplicant.create_wsc()

        for login in self.login_table.all():
            self.wpa_supplicant.add_network_to_wsc(login["ssid"], login["password"])

    @dispatch()
    def connect(self):
        """Method to try to connect to one of the available networks using wpa_supplicant.conf file that is restarted by subprocess.
        """

        if self.activity:
            if self.are_networks_accessible():
                self.wpa_supplicant.restart_ws_service()
                time.sleep(5)

            if self.is_connected_to_network():
                logger.info("Connected to a network.")
                return True

        return False

    @dispatch(str, str)
    def connect(self, ssid, password):
        """Method to try connect to one of available networks with using `wifi` library.

        Args:
            ssid (str):       	        The name of the surrounding access point.
            password (str):       	    The password of the surrounding access point.
        """
        result = False
        if self.activity:
            for cell in self.current_cells:
                if cell.ssid == ssid:
                    try:
                        scheme = Scheme.for_cell(self.wlan, ssid, cell, password)
                        scheme.activate()
                        result = True
                    except Exception as e:
                        logger.error(e)

        return result

    def try_creating_connection(self):
        """Method to try connect to one of available networks.
        """

        if self.activity:
            for network in self.known_networks:
                if self.connect(network["ssid"], network["password"]):
                    return True
        return False

    def login_upsert(self, ssid, password, force_insert=False):
        """Function to insert(or update) the connection info of new networks to the database.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        if self.login_table.search((Query().ssid == ssid)):
            if force_insert:
                # self.already_exist = False
                self.login_table.update({'password': password, 'wlan': self.wlan}, Query().ssid == ssid)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.login_table.insert({
                'wlan': self.wlan,
                'ssid': ssid,
                'password': password
            })  # insert the given data

        return ""

    def status_upsert(self, activity, force_insert=False):
        """Function to insert(or update) the status of NetworkConnector to the database.

        Args:
            activity (bool):        Activity flag of the NetworkConnector. If False, NetworkConnector not try connecting to surround networks.
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        status = self.status_table.all()

        if status:
            self.status_table.update({'activity': activity})
        else:
            self.status_table.insert({
                'activity': activity,
            })  # insert the given data

        return ""

    def __refresh_known_networks(self):
        """Method to refresh known networks from the database (and creating objects for them.)
        """

        self.known_networks.clear()

        for login in self.login_table.all():
            network = {"ssid": login["ssid"], "password": login["password"], "wlan": login["wlan"]}
            self.known_networks.append(network)

    @staticmethod
    def __restart_networking_service():
        """Method to to restart networking.service
        """
        call("systemctl restart networking.service", shell=True)

    def __refresh_status(self):
        """Method to refresh status from the database.
        """
        status = self.status_table.all()

        if status:
            self.activity = status[0]["activity"]
        else:
            self.activity = True

    def change_status(self, activity):
        """high-level method to change status of NetworkConnector via given parameters.

        Args:
            activity (bool):              Activity flag of the NetworkConnector. If False, NetworkConnector not try connecting to surround networks.

        Returns:
            str:  Response.
        """

        self.status_upsert(activity)
        self.__refresh_status()

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
            logger.info("No internet access!")
            pass
        return False

    @staticmethod
    def is_connected_to_network():
        """The top-level method to check network connection status using `hostname` command via subprocess.

        Returns:
            bool:  status.
        """
        wifi_ip = check_output(['hostname', '-I'])

        if wifi_ip:
            return True

        return False

    def are_networks_accessible(self):
        """The top-level method to check if T_System has the necessary information to connect to surrounding networks.

        Returns:
            bool:  status.
        """

        for known_network in self.known_networks:
            if known_network["ssid"] in self.current_available_networks:
                return True
        return False


class WpaSupplicant:
    """Class to define a wpa supplicant handler to managing wpa_supplicant.conf file for its headers and networks.

    This class provides necessary initiations and functions named :func:`t_system.accession.WpaSupplicant.add_network_to_wsc`
    as the record point the new network connection to the wpa_supplicant.conf file and named :func:`t_system.accession.WpaSupplicant.create_wsc`
    for creating wpa_supplicant.conf file with necessary headers.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.accession.WpaSupplicant` class.

        Args:
            args:                   Command-line arguments.
        """

        self.wpa_supp_conf_file = "/etc/wpa_supplicant/wpa_supplicant.conf"
        self.country_code = args["country_code"]
        self.wlan = args["wlan"]

        self.conf_headers = ["ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev", "update_config=1", f'country={self.country_code}']

        self.check_wsc()

    def check_wsc(self):
        """Method to check wpa_supplicant.conf file's validation. If the file is not valid, method creates new valid file.
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
                logger.info("wpa_supplicant.conf is not valid. Creating new one.")
                self.create_wsc()

        else:
            self.create_wsc()

    def restart_ws_service(self):
        """Method to restart wpa_supplicant service with reconfigured wpa_supplicant.conf file.
        """

        # call("rm -f /var/run/wpa_supplicant/wlan0", shell=True)
        call(f'wpa_supplicant -i {self.wlan} -c /etc/wpa_supplicant/wpa_supplicant.conf', shell=True)

    def create_wsc(self):
        """The high(and low)-level method to create initialization wpa_supplicant.conf file.
        """

        time.sleep(0.5)

        f = open(self.wpa_supp_conf_file, "w")
        f.write(self.conf_headers[0] + '\n')
        f.write(self.conf_headers[1] + '\n')
        f.write(self.conf_headers[2] + '\n')
        f.close()

        os.system('sudo chown root:root ' + self.wpa_supp_conf_file)
        os.system('sudo chmod 600 ' + self.wpa_supp_conf_file)

        if os.path.isfile(self.wpa_supp_conf_file):
            logger.info('wpa_supplicant.conf created successfully')

    def add_network_to_wsc(self, ssid, password, priority=None):
        """The high(and low)-level method to add new network ssid and psk information to wpa_supplicant.conf file.

        Args:
            ssid:       	        The name of the surrounding access point.
            password:       	    The password of the surrounding access point.
            priority (int):         The priority flag.
        """

        command_txt = f'sudo wpa_passphrase "{ssid}" "{password}"'

        result = check_output(command_txt, shell=True).decode("utf-8").splitlines()  # result = [['network={', '\tssid="SSID', '\t#psk="PASSWORD"', '\tpsk=PSK_OF_PASSWORD', '}']]

        f = open(self.wpa_supp_conf_file, 'a')
        f.write("\n")
        for line in result:
            if priority is not None and "}" in line:
                f.write(f'\tpriority={priority}\n')
            f.write(f'{line}\n')
        f.close()
