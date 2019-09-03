#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: database
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's database and table creation ability. Powered by TinyDB.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import TinyDB  # TinyDB is a lightweight document oriented database


class DBFetcher:
    """Class to define an database handler with given folder and table name. It's only job creating databases or tables and returning them.

    This class provides necessary initiations and functions named :func:`t_system.database.Database.get`
    for return TinyDB database object.
    """

    def __init__(self, folder, name, table=None, cache_size=None):
        """Initialization method of :class:`t_system.database.Database` class.

        Args:
            folder (str)                    Folder that contains database.
            name (str)                      Name of the database.
            table (str):                    Current working table name.
            cache_size (int):               TinyDB caches query result for performance.
        """

        self.folder = folder
        self.name = name
        self.table = table
        self.cache_size = cache_size

    def fetch(self):
        """Method to return database. If there is a table name method  creates a table and returns that. Otherwise returns all db.

        Returns:
                TinyDB: database object.
        """

        db = TinyDB(f'{self.folder}/{self.name}.json')

        if self.table:
            return self.__set_table(db, self.table, self.cache_size)

        return db

    @staticmethod
    def __set_table(db, table_name, cache_size=None):
        """Method to set database by table name.

        Args:
            db (TinyDB):                    TinyDB object.
            table_name (str):               Current working table name.
            cache_size (int):               TinyDB caches query result for performance.
        """

        return db.table(table_name, cache_size=cache_size)
