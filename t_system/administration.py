#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: administration
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's accessing external network and creating internal network(becoming access point) ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import hashlib
import secrets
import string

from t_system.db_fetching import DBFetcher
from t_system import dot_t_system_dir


class Identifier:
    """Class to define an identifier for creating and handling an idenditity to T_System.

    This class provides necessary initiations and functions named :func:`t_system.administration.Administrator.change_keys`
    for changing admin entry keys.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.administration.Identifier` class.
        """

        self.table = DBFetcher(dot_t_system_dir, "db", "identity").fetch()

        self.public_id = None
        self.private_id = None
        self.name = None

        self.__get_keys()

    def show_keys(self):
        """Method to print identification keys to the console.
        """

        print(f'public id is {self.public_id},\nprivate id is {self.private_id},\nname is {self.name}')

    def change_keys(self, public_id=None, private_id=None, name=None):
        """Method to change keys of identity for unique identification of T_System. 2 key(id and name) identification.

        Args:
            public_id:    	    Public id of the T_System itself.
            private_id:    	    Private id of the T_System itself.
            name:     	        Specified name of the T_System itself.
        """

        if public_id is None and private_id is None and name is None:
            return False

        if public_id:
            self.public_id = public_id

        if private_id:
            self.private_id = private_id

        if name:
            self.name = name

        self.__db_upsert(self.public_id, self.private_id, self.name)

        return True

    def __get_keys(self):
        """Method to get keys of identity from database.
        """
        identity = self.table.all()

        if identity:
            identity = identity[0]  # table.all() return a list. But there is just 1 identity.
            self.public_id = identity["public_id"]
            self.private_id = identity["private_id"]
            self.name = identity["name"]
        else:
            self.__set_default_identity()

    def __set_default_identity(self):
        """Method to set keys of identity for default identity specification. If not changed or added yet.
        """

        self.public_id = self.get_random_id(6)
        self.private_id = self.get_random_id(6)
        self.name = f'T_System-{self.public_id}'

        self.__db_upsert(self.public_id, self.private_id, self.name)

    def __db_upsert(self, public_id, private_id, name):
        """Function to insert(or update) the position to the database.

        Args:
            public_id:    	    Public id of the T_System itself.
            private_id:    	    Private id of the T_System itself.
            name:     	        Specified name of the T_System itself.

        Returns:
            str:  Response.
        """

        identity = self.table.all()

        if identity:
            self.table.update({'public_id': public_id, 'private_id': private_id, 'name': name})
        else:
            self.table.insert({
                'public_id': public_id,
                'private_id': private_id,
                'name': name
            })  # insert the given data

        return ""

    def get_random_id(self, digit_number=6):
        """Method to set keys of identity for default identity specification. If not changed or added yet.

        Args:
            digit_number:    	        number of T_System id digits.
        """

        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(digit_number))


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

        self.__get_keys()

    def change_keys(self, ssid, password):
        """Method to change keys of secret entry point for root authorized. 2 key(ssid and password) authentication uses sha256 encryption.

        Args:
            ssid:       	        Administration ssid.
            password:       	    Administration ssid.
        """

        ssid_hash = hashlib.sha256(ssid.encode()).hexdigest()
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        public_key = hashlib.sha256((ssid + password).encode()).hexdigest()
        private_key = hashlib.sha256(public_key.encode()).hexdigest()

        self.__db_upsert(ssid_hash, password_hash, private_key)

    def __get_keys(self):
        """Method to get keys of secret entry point from database.
        """
        admin = self.table.all()

        if admin:
            admin = admin[0]  # table.all() return a list. But there is just 1 admin.
            self.ssid_hash = admin["ssid"]
            self.password_hash = admin["password"]
            self.private_key = admin["private_key"]
        else:
            self.__set_default_admin()

    def __set_default_admin(self):
        """Method to set keys of secret entry point for default root authorized. If not changed or added yet.
        """
        self.ssid_hash = "da8cb7b1563da30fb970b2b0358c3fd43e688f89c681fedfb80d8a3777c20093"
        self.password_hash = "135e1d0dd3e842d0aa2c3144293f84337b0907e4491d47cb96a4b8fb9150157d"
        self.private_key = "453bc4f4eb1415d7a1ffff595cc98bf2b538af443d57e486e71b88c966934010"

        self.__db_upsert(self.ssid_hash, self.password_hash, self.private_key)

    def __db_upsert(self, ssid_hash, password_hash, private_key):
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
    """Method to create secret entry point for root authorized. 2 key(ssid and password) authentication uses sha256 encryption.

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
    """Method for checking whether the man who submitted the requests has administrative authority.

    Args:
        admin_id:       	    The id of the admin that is created from check_secret_root_entry method.
    """

    if admin_id:
        from t_system import administrator

        if hashlib.sha256(admin_id.encode()).hexdigest() == administrator.private_key:
            return True

    return False
