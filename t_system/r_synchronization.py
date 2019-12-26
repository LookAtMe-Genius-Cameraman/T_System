#!/usr/bin/python3
# -*- coding: utf-8 -*-
# few part of this code that about Dropbox integration taken from https://github.com/dropbox/dropbox-sdk-python/blob/master/example/updown.py

"""
.. module:: r_synchronization
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's remote storage synchronization feature.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os  # Miscellaneous operating system interfaces
import datetime  # Basic date and time types
import time  # Time access and conversions
import unicodedata
import dropbox

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher

from t_system import network_connector

from t_system import dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class RSynchronizer:
    """Class to define a remote storage synchronization ability with some cloud platforms of T_System.

    This class provides necessary initiations and functions named :func:`t_system.r_sync.RSynchronizer.start_sync`
    for provide starting the folder synchronization with specified cloud storage services.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.r_sync.RSynchronizer` class.
        """

        self.services_table = DBFetcher(dot_t_system_dir, "db", "r_sync").fetch()

        self.services = []

        self.__set_services()

        if not self.services:
            self.__create_services()

    def start_sync(self, service_name=None, account_name=None):
        """Method to start synchronization of the recorded videos with specified remote storage.

         Args:
                service_name (str):     Name of the service.
                account_name (str):     Name of the one of service account.
        """

        result = True

        if service_name and account_name:
            for service in self.services:
                if service_name == service.name:
                    service.activate_account(account_name)
                    service.sync()

        elif not (service_name or account_name):
            for service in self.services:
                if service.to_be_used:
                    service.sync()
        else:
            logger.critical(f'`service_name` and `account_name` parameters have to be given together.')
            result = False

        return result

    def stop_sync(self):
        """Method to stop folder synchronization.
        """

        pass

    @staticmethod
    def is_sync_available():
        """Method to check the synchronization's availability about networks connection.
        """

        return network_connector.is_network_online()

    def get_services(self, service_names=None):
        """Method to get existing service in given name. If service_names is None it returns all services.

         Args:
                service_names (list):           Name list of the services.
        """
        services = []

        if service_names:
            for service_name in service_names:
                for service in self.services:
                    if service.name == service_name:
                        services.append(service)
            return services

        return self.services

    def set_service_usage_stat(self, service_name, to_be_used):
        """Method to set given usage status of service as to be used or not to be used.

         Args:
                service_name (str):     Name of the service.
                to_be_used (bool):      To be used flag that specify usage status of service on folder synchronization.
        """

        for service in self.services:
            if service_name == service.name:
                service.set_usage_stat(to_be_used)
                return True
        return False

    def activate_service_account(self, service_name, account_name):
        """Method to set given access key for using on the current remote storage service.

         Args:
                service_name (str):     Name of the service.
                account_name (str):     Name of the one of service account.
        """

        for service in self.services:
            if service_name == service.name:
                service.activate_account(account_name)
                return True
        return False

    def set_service_account(self, service_name, account):
        """Method to add or update personal account information to the given service_name's service.

         Args:
                service_name (str):     Name of the service.
                account (dict):         Identity information of websites stream.
        """

        for service in self.services:
            if service_name == service.name:
                service.upsert_account(account["account_name"], account["key"])
                return True
        return False

    def remove_service_account(self, service_name, account_name):
        """Method to remove personal account information to the given service_name's service.

         Args:
                service_name (str):     Name of the service.
                account_name (str):     Name of the one of service account.
        """

        for service in self.services:
            if service_name == service.name:
                service.remove_account(account_name)
                return True
        return False

    def refresh_services(self):
        """Method to refresh existing websites on runtime alterations.
        """

        self.services.clear()
        self.__set_services()

    def show_services(self, service_names=None):
        """Method to show existing service in given name. If service_names is None it returns all services.

         Args:
                service_names (list):           Name list of the services.
        """

        from tabulate import tabulate

        services = []

        for service in self.get_services(service_names):
            services.append([service.name, service.to_be_used])

        print(tabulate(services, headers=["Name", "Usage Status"]))

    def show_accounts(self, service_names=None):
        """Method to show existing accounts of service in given name. If service_names is None it returns all accounts.

         Args:
                service_names (list):           Name list of the services.
        """

        from tabulate import tabulate

        accounts = []

        for service in self.get_services(service_names):

            website_name = service.name

            for account in service.accounts:
                accounts.append([website_name, account["name"], account["key"]])

                website_name = ""

        print(tabulate(accounts, headers=["Website Name", "Account Name", "Key"]))

    def __create_services(self):
        """Method to create remote synchronizer services if there is no services created yet.
        """

        self.services.append(DropBox())

    def __set_services(self):
        """Method to set existing remote synchronizer services.
        """

        for service in self.services_table.all():
            if service["name"] == "Dropbox":

                self.services.append(DropBox(service["info"]["to_be_used"], service["info"]["accounts"], service["info"]["active_account"]))


class DropBox:
    """Class to define a file synchronizer to an Dropbox account.

    This class provides necessary initiations and functions named :func:`t_system.r_sync.DropBox.sync`
    to provide synchronizing recorded videos with the Dropbox account.
    """

    def __init__(self, to_be_used=False, accounts=None, active_account=None):
        """Initialization method of :class:`t_system.r_sync.DropBox` class.

        Args:
                to_be_used (bool):      To be used flag that specify usage status of service on folder synchronization.            
                accounts:               DropBox account owner name and account API key list.
                active_account:       hexadecimal stream key that use in current stream of the website.
        """

        self.accounts = accounts
        if not accounts:
            self.accounts = []

        self.active_account = active_account
        if not active_account:
            self.active_account = {}

        self.name = "Dropbox"
        self.to_be_used = to_be_used

        self.dbx = None

        self.sync_sou_dir = f'{dot_t_system_dir}/records'
        self.sync_tar_dir = "Media-from-T_System"

        self.table = DBFetcher(dot_t_system_dir, "db", "r_sync").fetch()

        self.__db_upsert()

    def sync(self):
        """Method to synchronizing folder that keeps recorded videos with user's Dropbox account.
        """

        if self.__prepare_sync():

            for dn, dirs, files in os.walk(self.sync_sou_dir):
                sub_folder = dn[len(self.sync_sou_dir):].strip(os.path.sep)
                listing = self.list_folder(self.sync_tar_dir, sub_folder)
                logger.info('Descending into', sub_folder, '...')

                # First do all the files.
                for file in files:
                    file_path = os.path.join(dn, file)

                    if isinstance(file, bytes):
                        file = file.decode('utf-8')

                    n_name = unicodedata.normalize('NFC', file)

                    if file.startswith('.'):
                        logger.info('Skipping dot file:', file)

                    elif file.startswith('@') or file.endswith('~'):
                        logger.info('Skipping temporary file:', file)

                    elif file.endswith('.pyc') or file.endswith('.pyo'):
                        logger.info('Skipping generated file:', file)

                    elif file.endswith('.json'):
                        logger.info('Skipping database file:', file)

                    elif n_name in listing:

                        md = listing[n_name]
                        mtime = os.path.getmtime(file_path)
                        mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                        size = os.path.getsize(file_path)

                        if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                            logger.info(f' {file} is already synced [stats match]')

                        else:
                            logger.info(file, f'{file} exists with different stats, downloading')
                            res = self.download(self.sync_tar_dir, sub_folder, file)

                            with open(file_path) as f:
                                data = f.read()

                            if res == data:
                                logger.info(f'{file} is already synced [content match]')
                            else:
                                logger.info(f'{file} has changed since last sync')
                                self.upload(file_path, self.sync_tar_dir, sub_folder, file, overwrite=True)
                    else:
                        self.upload(file_path, self.sync_tar_dir, sub_folder, file)

                # Then choose which subdirectories to traverse.
                keep = []
                for directory in dirs:
                    if directory.startswith('.'):
                        logger.info(f'Skipping dot directory: {directory}')
                    elif directory.startswith('@') or directory.endswith('~'):
                        logger.info(f'Skipping temporary directory: {directory}')
                    elif directory == '__pycache__':
                        logger.info(f'Skipping generated directory: {directory}')
                    else:
                        logger.info(f'Keeping directory: {directory}')
                        keep.append(directory)
                dirs[:] = keep

    def __prepare_sync(self):
        """Method to prepare DropBoxer to folder synchronization.
        """

        if self.activate_account:
            self.dbx = dropbox.Dropbox(self.active_account["key"])
            return True

        return False

    def list_folder(self, folder, sub_folder):
        """Method to list a folder.

        Args:
                folder (str):          Top-folder that contains synchronized items.
                sub_folder (str):      Sub-folder that belongs to top-folder.
        Returns:
                a dict mapping unicode filenames to FileMetadata|FolderMetadata entries.
        """
        path = '/%s/%s' % (folder, sub_folder.replace(os.path.sep, '/'))
        while '//' in path:
            path = path.replace('//', '/')
        path = path.rstrip('/')

        try:
            res = self.dbx.files_list_folder(path)
        except dropbox.exceptions.ApiError as err:
            logger.error('Folder listing failed for', path, '-- assumed empty:', err)
            return {}
        else:
            rv = {}
            for entry in res.entries:
                rv[entry.name] = entry
            return rv

    def download(self, folder, sub_folder, file_name):
        """Method to download a file from Dropbox account.

        Args:
                folder (str):          Top-folder that contains synchronized items.
                sub_folder (str):      Sub-folder that belongs to top-folder.
                file_name (str):       The name of the file that will be uploaded.

        Returns:
                The bytes of the file, or None if it doesn't exist.
        """
        path = '/%s/%s/%s' % (folder, sub_folder.replace(os.path.sep, '/'), file_name)
        while '//' in path:
            path = path.replace('//', '/')

        try:
            md, res = self.dbx.files_download(path)

        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None

        data = res.content
        logger.info(f'{len(data)} bytes; md: {md}')

        return data

    def upload(self, file_path, folder, sub_folder, file_name, overwrite=False):
        """Method to upload a file to Dropbox account.

        Args:
                file_path (str):       The path of the file that will be uploaded.
                folder (str):          Top-folder that contains synchronized items.
                sub_folder (str):      Sub-folder that belongs to top-folder.
                file_name (str):       The name of the file that will be uploaded.
                overwrite (bool):      The overwriting flag of file that will be uploaded.

        Returns:
                The request response, or None in case of error.
        """

        path = '/%s/%s/%s' % (folder, sub_folder.replace(os.path.sep, '/'), file_name)
        while '//' in path:
            path = path.replace('//', '/')

        mode = (dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add)

        mtime = os.path.getmtime(file_path)

        with open(file_path, 'rb') as f:
            data = f.read()

        try:
            res = self.dbx.files_upload(data, path, mode, client_modified=datetime.datetime(*time.gmtime(mtime)[:6]), mute=True)

        except dropbox.exceptions.ApiError as err:

            logger.error(f'API error {err}')
            return None
        logger.info(f'uploaded as {res.name.encode("utf8")}')

        return res

    def set_usage_stat(self, to_be_used):
        """Method to set website as to be used or not to be used.

        Args:
                to_be_used (bool):      To be used flag that specify usage status of service on folder synchronization.
        """

        self.to_be_used = to_be_used

        self.__db_upsert(force_insert=True)

    def activate_account(self, account_name):
        """Method to set given API key of given account for using on the current folder synchronization.

        Args:
            account_name (str):         Name of the Dropbox account.
        """

        for account in self.accounts:
            if account["is_active"]:
                account["is_active"] = False
                break

        for account in self.accounts:
            if account["account_name"] == account_name:

                account["is_active"] = True

                self.active_account = account
                self.__db_upsert(force_insert=True)

            return True

        return False

    def upsert_account(self, name, key):
        """Method to insert(or update) new API key and its account name for reaching the Dropbox.

        Args:
            name (str):                 Name of the Dropbox account.
            key (str):                  API key of Dropbox account.
        """
        is_update = False

        for account in self.accounts:
            if name == account["name"]:
                account["key"] = key
                is_update = True
                break

        if not is_update:
            self.accounts.append({"name": name, "key": key, "is_active": False})

        self.__db_upsert(force_insert=True)

        return True

    def remove_account(self, name):
        """Method to remove existing stream key and its account name.

        Args:
            name (str):                 Name of the Dropbox account.
        """

        for account in self.accounts:
            if name == account["name"]:
                self.accounts.remove(account)  # for removing object from list
                self.__db_upsert(force_insert=True)

                return True
        return False

    def delete_self(self):
        """Method to delete website itself.
        """
        self.table.remove((Query().service == self.name))

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):        Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().service == self.name)):
            if force_insert:
                self.table.update({'info': {'to_be_used': self.to_be_used, 'accounts': self.accounts, 'active_account': self.active_account}}, Query().service == self.name)

            else:
                return "Already Exist"
        else:
            self.table.insert({
                'name': self.name,
                'info': {
                    'to_be_used': self.to_be_used,
                    'accounts': self.accounts,
                    'active_account': self.active_account
                }
            })  # insert the given data

        return ""
