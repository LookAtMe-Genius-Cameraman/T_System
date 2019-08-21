#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: administration
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's accessing external network and creating internal network(becoming access point) ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import hashlib

from t_system.db_fetching import DBFetcher
from t_system import dot_t_system_dir


class Administrator:
    """Class to define an administrator for managing admin authentication keys of tracking system.

    This class provides necessary initiations and functions named :func:`t_system.administration.Administrator.change_keys`
    for changing admin entry keys.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.administration.Administrator` class.
        """

        self.table = DBFetcher(dot_t_system_dir, "db", "admin").fetch()

        self.ssid_hash = None
        self.password_hash = None
        self.private_key = None

        self.get_keys()

    def change_keys(self, ssid, password):
        """The high-level method to change keys of secret entry point for root authorized. 2 key(ssid and password) authentication uses sha256 encryption.

        Args:
            ssid:       	        Administration ssid.
            password:       	    Administration ssid.
        """

        ssid_hash = hashlib.sha256(ssid.encode()).hexdigest()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        public_key = hashlib.sha256((ssid + password).encode()).hexdigest()
        private_key = hashlib.sha256(public_key.encode()).hexdigest()

        self.db_upsert(ssid_hash, password_hash, private_key)

    def get_keys(self):
        """The low-level method to get keys of secret entry point from database.
        """
        admin = self.table.all()

        if admin:
            admin = admin[0]  # table.all() return a list. But there is just 1 admin.
            self.ssid_hash = admin["ssid"]
            self.password_hash = admin["password"]
            self.private_key = admin["private_key"]
        else:
            self.set_default_admin()

    def set_default_admin(self):
        """The low-level method to set keys of secret entry point for default root authorized. If not changed or added yet.
        """
        self.ssid_hash = "da8cb7b1563da30fb970b2b0358c3fd43e688f89c681fedfb80d8a3777c20093"
        self.password_hash = "135e1d0dd3e842d0aa2c3144293f84337b0907e4491d47cb96a4b8fb9150157d"
        self.private_key = "453bc4f4eb1415d7a1ffff595cc98bf2b538af443d57e486e71b88c966934010"

        self.db_upsert(self.ssid_hash, self.password_hash, self.private_key)

    def db_upsert(self, ssid_hash, password_hash, private_key,):
        """Function to insert(or update) the position to the database.

        Args:
            ssid_hash:    	        Administration ssid key hash.
            password_hash:     	    Administration password key hash.
            private_key:     	    Administration private key.

        Returns:
            str:  Response.
        """

        admin = self.table.all()

        if admin:
            self.table.update({'ssid': ssid_hash, 'password': password_hash, 'private_key': private_key})
        else:
            self.table.insert({
                'ssid': ssid_hash,
                'password': password_hash,
                'private_key': private_key
            })  # insert the given data

        return ""


def check_secret_root_entry(ssid, password):
    """The high-level method to create secret entry point for root authorized. 2 key(ssid and password) authentication uses sha256 encryption.

    Args:
        ssid:       	        The name of the surrounding access point.
        password:       	    The password of the surrounding access point.
    """
    from t_system import administrator

    admin = {"ssid": administrator.ssid_hash, "passwords": administrator.password_hash}

    ssid_hash = hashlib.sha256(ssid.encode())
    password_hash = hashlib.sha256(password.encode())

    quest = {"ssid": ssid_hash.hexdigest(), "passwords": password_hash.hexdigest()}

    if admin == quest:
        admin_id = hashlib.sha256((ssid + password).encode()).hexdigest()  # admin_id is the public key
        return admin_id

    return False


def is_admin(admin_id):
    """the high-level method for checking whether the man who submitted the requests has administrative authority.

    Args:
        admin_id:       	    The id of the admin that is created from check_secret_root_entry method.
    """

    if admin_id:
        from t_system import administrator

        if hashlib.sha256(admin_id.encode()).hexdigest() == administrator.private_key:
            return True

    return False
