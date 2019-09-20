#!/usr/bin/python3
# -*- coding: utf-8 -*-
# most part of this code taken from https://gist.github.com/egorf/66d88056a9d703928f93
# Copyright (c) 2015, Emlid Limited

"""
.. module:: bluetoothctl
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's accessing to bluetooth devices like headsets.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import time  # Time access and conversions
import os  # Miscellaneous operating system interfaces
import pexpect
import subprocess
import sys


class BluetoothctlError(Exception):
    """Class to define an exception that is raised, when bluetoothctl fails to start.
    """
    pass


class Bluetoothctl:
    """Class to define a wrapper for bluetoothctl utility.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.accession.Bluetoothctl` class.
        """

        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", echo=False)

    def get_output(self, command, pause=0):
        """Methow to run a command in bluetoothctl prompt and return its output as a list of lines.

        Args:
            command:       	        command that will send to pexpect instance.
            pause:       	        delay time between sending command and catching the its return.
        """
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n".encode("utf-8"))

    def start_scan(self):
        """Method to Start bluetooth scanning process.
        """
        try:
            out = self.get_output("scan on")
        except BluetoothctlError as e:
            print(e)
            return None

    def make_discoverable(self):
        """Method to make the device discoverable.
        """
        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError as e:
            print(e)
            return None

    @staticmethod
    def parse_device_info(info):
        """Method to parse a string corresponding to a device.

        Args:
            info (str):       	    information block of device.
        """

        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info for keyword in block_list)

        if string_valid:
            try:
                device_position = info.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info[device_position:].split(" ", 2)
                    device = {
                        "mac_address": attribute_list[1],
                        "name": attribute_list[2]
                    }

        return device

    def get_available_devices(self):
        """Method to return a list of tuples of paired and discoverable devices.
        """
        try:
            out = self.get_output("devices")
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line.decode("utf-8"))
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """Method to return a list of tuples of paired devices.
        """
        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line.decode("utf-8"))
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """Method to filter paired devices out of available.
        """
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def get_device_info(self, mac_address):
        """Method to get device info by mac address.

        Args:
            mac_address (str):      mac address of the device.
        """
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            return out

    def pair(self, mac_address):
        """Method to pair with a device by mac address.

        Args:
            mac_address (str):      mac address of the device.
        """
        try:
            out = self.get_output("pair " + mac_address, 4)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def remove(self, mac_address):
        """,Method to remove paired device by mac address and return success of the operation.

        Args:
            mac_address (str):      mac address of the device.
        """
        try:
            out = self.get_output("remove " + mac_address, 3)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["not available", "Device has been removed", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self, mac_address):
        """Method to connect to a device by mac address.

        Args:
            mac_address (str):      mac address of the device.
        """
        try:
            out = self.get_output("connect " + mac_address, 2)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self, mac_address):
        """Method to disconnect to a device by mac address.

        Args:
            mac_address (str):      mac address of the device.
        """
        try:
            out = self.get_output("disconnect " + mac_address, 2)
        except BluetoothctlError as e:
            print(e)
            return None
        else:
            res = self.child.expect(["Failed to disconnect", "Successful disconnected", pexpect.EOF])
            success = True if res == 1 else False
            return success


if __name__ == "__main__":

    print("Init bluetooth...")
    bl = Bluetoothctl()
    print("Ready!")
    bl.start_scan()
    print("Scanning for 10 seconds...")
    for i in range(0, 10):
        print(i)
        time.sleep(1)

    print(bl.get_discoverable_devices())






