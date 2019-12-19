#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: online_stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's online stream broadcast feature.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os  # Miscellaneous operating system interfaces
import uuid  # The random id generator
import subprocess  # Subprocess managements
import json

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher

from t_system import network_connector

from t_system import T_SYSTEM_PATH, dot_t_system_dir
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class OnlineStreamer:
    """Class to define an online stream ability to famous platforms of T_System.

    This class provides necessary initiations and functions named :func:`t_system.online_stream.OnlineStream.set_set_parameters`
    as the external setting point of the access point utilities.
    """

    def __init__(self, camera, hearer):
        """Initialization method of :class:`t_system.online_stream.OnlineStream` class.

        Args:
                camera:       	        Camera object from PiCamera.
                hearer:       	        Hearer object.
        """

        self.folder = f'{dot_t_system_dir}/streaming'

        self.__check_folders()

        self.websites_table = DBFetcher(self.folder, "db", "websites").fetch()

        self.websites = []
        self.stream_pipes = []

        self.streamer_config_file = f'{T_SYSTEM_PATH}/online_stream/config.json'

        self.__set_websites()

        if not self.websites:
            self.__create_websites()

        self.camera = camera
        self.hearer = hearer

    def prepare_stream(self):
        """Method to prepare live stream parameters.
        """

        common_stream_cmd = "ffmpeg -f h264 -r 25 -i - -itsoffset 5.5 -fflags nobuffer -f alsa -ac 1 -i hw:1,0 -vcodec copy -acodec aac -ac 1 -ar 8000 -ab 32k -map 0:0 -map 1:0 -strict experimental -f flv"

        for website in self.websites:
            if website.to_be_used:

                stream_cmd = f'{common_stream_cmd} {website.server}{website.active_stream_id["key"]}'

                self.stream_pipes.append(subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE))

    def go_live(self):
        """Method to start live stream by OnlineStreamer's members.
        """

        self.prepare_stream()

        for stream_pipe in self.stream_pipes:
            self.camera.start_recording(stream_pipe.stdin, format='h264', bitrate=2000000)

    def stop_live(self):
        """Method to stop live stream.
        """

        self.camera.stop_recording()

        for stream_pipe in self.stream_pipes:

            stream_pipe.stdin.close()
            stream_pipe.wait()

    @staticmethod
    def is_stream_available():
        """Method to check the stream's availability about networks connection.
        """

        return network_connector.is_network_online()

    def get_websites(self, w_ids=None):
        """Method to get existing website in given id. If w_id is None it returns all websites.

         Args:
                w_ids (list):           ID list of the websites.
        """
        websites = []

        if w_ids:
            for w_id in w_ids:
                for website in self.websites:
                    if website.id == w_id:
                        websites.append(website)
            return websites

        return self.websites

    def set_website_usage_stat(self, w_id, to_be_used):
        """Method to set given usage status of website as to be used or not to be used.

         Args:
                w_id (str):             ID of the website.
                to_be_used (bool):      To be used flag that specify usage status of website on live stream.
        """
        
        for website in self.websites:
            if w_id == website.id:
                website.set_usage_stat(to_be_used)
                return True

        return False

    def activate_website_stream(self, w_id, stream_acc_name):
        """Method to set given stream key for using on the current live stream for the website.

         Args:
                w_id (str):             ID of the website.
                stream_acc_name (str):  Account name of the stream.
        """

        for website in self.websites:
            if w_id == website.id:
                website.activate_stream_key(stream_acc_name)
                return True

        return False

    def set_website_stream(self, w_id, stream_id):
        """Method to add or update personal stream information to the given w_id's website.

         Args:
                w_id (str):             ID of the website.
                stream_id (dict):       Identity information of websites stream.
        """

        for website in self.websites:
            if w_id == website.id:
                website.upsert_stream_key(stream_id["account_name"], stream_id["key"])
                return True

        return False

    def remove_website_stream(self, w_id, stream_acc_name):
        """Method to remove personal stream information to the given w_id's website.

         Args:
                w_id (str):             ID of the website.
                stream_acc_name (str):  Account name of the stream.
        """

        for website in self.websites:
            if w_id == website.id:
                website.remove_stream_key(stream_acc_name)
                return True

        return False

    def refresh_websites(self):
        """Method to refresh existing websites on runtime alterations.
        """

        self.websites.clear()
        self.__set_websites()

    def add_website(self, name, url, server, force_insert=False):
        """Method to create websites by given parameters to the `config.json` file.

        Args:
                name:                   Name of the WebSite. youtube, facebook etc.
                url:                    Website's page URL.
                server:                 Website's Live stream server RTMP URL.
                force_insert (bool):    Force insert flag.
        """
        is_website_exist = False

        with open(self.streamer_config_file) as conf_file:
            config = json.load(conf_file)

            for website_conf in config["available_websites"]:
                if website_conf["name"] == name:
                    is_website_exist = True

                    if force_insert:
                        website_conf["url"] = url
                        website_conf["server"] = server

                        for website in self.websites:
                            if website.name == name:
                                website.update_self(url, server)
                                break
                    break

            if not is_website_exist:
                config["available_websites"].append({"name": name, "url": url, "server": server})

            conf_file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(config, conf_file, indent=4)
            conf_file.truncate()  # remove remaining part

            self.refresh_websites()
            return True

    def remove_websites(self, w_ids):
        """Method to create websites by given parameters to the `config.json` file.

        Args:
                w_ids (list):                   ID list of the WebSites. youtube, facebook etc.
        """

        result = False

        with open(self.streamer_config_file) as conf_file:
            config = json.load(conf_file)

        for website_conf in config["available_websites"]:
            for website_id in w_ids:
                for website in self.websites:
                    if website_id == website.id:
                        if website_conf["name"] == website.name:

                            website.delete_self()
                            self.websites.remove(website)

                            config["available_websites"].remove(website_conf)  # for removing object from list

                            conf_file.seek(0)  # <--- should reset file position to the beginning.
                            json.dump(config, conf_file, indent=4)
                            conf_file.truncate()  # remove remaining part

                            result = True
                            break
        if result:
            self.refresh_websites()

        return result

    def show_websites(self, w_ids=None):
        """Method to show existing website in given id. If w_id is None it returns all websites.

         Args:
                w_ids (list):           ID list of the websites.
        """
        from tabulate import tabulate

        websites = []

        for website in self.get_websites(w_ids):
            websites.append([website.id, website.name, website.url, website.server])

        print(tabulate(websites, headers=["ID", "Name", "URL", "Server"]))

    def show_stream_ids(self, w_ids=None):
        """Method to show existing stream IDs of website in given id. If w_id is None it returns all stream IDs.

         Args:
                w_ids (list):           ID list of the websites.
        """
        from tabulate import tabulate

        stream_ids = []

        for website in self.get_websites(w_ids):

            website_id = website.id
            website_name = website.name

            for stream_id in website.stream_ids:

                stream_ids.append([website_id, website_name, stream_id["account_name"], stream_id["key"]])

                website_id = ""
                website_name = ""

        print(tabulate(stream_ids, headers=["Website ID", "Website Name", "Account Name", "Key"]))

    def __create_websites(self):
        """Method to create websites by config.json file.
        """

        with open(self.streamer_config_file) as conf_file:
            available_websites = json.load(conf_file)["available_websites"]

        for website in available_websites:
            self.websites.append(StreamWebSite(website["name"], website["url"], website["server"]))

    def __set_websites(self):
        """Method to set existing websites.
        """

        for website in self.websites_table.all():
                self.websites.append(StreamWebSite(website["name"], website["url"], website["server"], website["to_be_used"], website["stream_ids"], website["active_stream_id"], website["id"]))

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)


class StreamWebSite:
    """Class to define website that will used as live stream platform.

    This class provides necessary initiations and functions named :func:`t_system.online_stream.StreamWebSite.set_set_parameters`
    as the external setting point of the access point utilities.
    """

    def __init__(self, name, url, server, to_be_used=False, stream_ids=None, active_stream_id=None, id=None):
        """Initialization method of :class:`t_system.online_stream.OnlineStream` class.

        Args:
                name:                   Name of the WebSite. youtube, facebook etc.
                url:                    Website's page URL.
                server:                 Website's Live stream server RTMP URL.
                to_be_used (bool):      To be used flag that specify usage status of website on live stream.
                stream_ids:             hexadecimal stream keys of the website.
                active_stream_id:       hexadecimal stream key that use in current stream of the website.
                id:                     Unique ID of the website.
        """

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.stream_ids = stream_ids
        if not stream_ids:
            self.stream_ids = []
            
        self.active_stream_id = active_stream_id
        if not active_stream_id:
            self.active_stream_id = {}

        self.name = name
        self.url = url
        self.server = server

        self.to_be_used = to_be_used

        self.streaming_folder = f'{dot_t_system_dir}/streaming'
        self.keys_folder = f'{self.streaming_folder}/keys'
        self.parent_folder = f'{self.streaming_folder}/websites'
        self.folder = f'{self.parent_folder}/{self.name}'

        self.key_file = f'{self.keys_folder}/{self.name}.key'

        self.__check_folders()

        self.table = DBFetcher(self.streaming_folder, "db", "websites").fetch()

        self.__db_upsert()

    def set_usage_stat(self, to_be_used):
        """Method to set website as to be used or not to be used.

        Args:
                to_be_used (bool):      To be used flag that specify usage status of website on live stream.
        """

        self.to_be_used = to_be_used

        self.__db_upsert(force_insert=True)

    def activate_stream_key(self, account_name):
        """Method to set given stream key for using on the current live stream for the website.

        Args:
            account_name (str):         Name of the website's account.
        """
        for stream_id in self.stream_ids:
            if stream_id["is_active"]:
                stream_id["is_active"] = False
                break

        for stream_id in self.stream_ids:
            if stream_id["account_name"] == account_name:
                with open(self.key_file, "w+") as key_file:
                    key_file.write(stream_id["key"])
                    key_file.close()

                stream_id["is_active"] = True

                self.active_stream_id = stream_id
                self.__db_upsert(force_insert=True)

            return True

        return False

    def upsert_stream_key(self, account_name, key):
        """Method to insert(or update) new stream key and its account name.

        Args:
            account_name (str):         Name of the website's account.
            key (str):                  Hexadecimal live stream key of the websites's account.
        """
        is_update = False

        for stream_id in self.stream_ids:
            if account_name == stream_id["account_name"]:
                stream_id["key"] = key
                is_update = True
                break

        if not is_update:
            self.stream_ids.append({"account_name": account_name, "key": key, "key_file": f'{self.folder}/{account_name}.key', "is_active": False})

        self.__db_upsert(force_insert=True)
        self.__set_key_files(account_name)

        return True

    def remove_stream_key(self, account_name):
        """Method to remove existing stream key and its account name.

        Args:
            account_name (str):         Name of the website's account.
        """

        for stream_id in self.stream_ids:
            if account_name == stream_id["account_name"]:
                self.stream_ids.remove(stream_id)  # for removing object from list
                self.__db_upsert(force_insert=True)
                os.remove(stream_id["key_file"])

                return True

        return False

    def update_self(self, url, server):
        """Method to update website itself.
        """
        if url:
            self.url = url

        if server:
            self.server = server

        self.__db_upsert(force_insert=True)

    def delete_self(self):
        """Method to delete website itself.
        """
        self.table.remove((Query().id == self.id))

    def __db_upsert(self, force_insert=False):
        """Function to insert(or update) the record to the database.

        Args:
            force_insert (bool):        Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().id == self.id)):
            if force_insert:
                self.table.update({'id': self.id, 'name': self.name, 'url': self.url, 'server': self.server, 'to_be_used': self.to_be_used, 'stream_ids': self.stream_ids, 'active_stream_id': self.active_stream_id}, Query().id == self.id)

            else:
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'url': self.url,
                'server': self.server,
                'to_be_used': self.to_be_used,
                'stream_ids': self.stream_ids,
                'active_stream_id': self.active_stream_id
            })  # insert the given data

        return ""

    def __set_key_files(self, account_name=None):
        """Method to crete `.key` files that keeps stream keys of the websites live stream entry.

        Args:
            account_name (str):         Name of the website's account.
        """
        result = False
        stream_ids = []

        if account_name:
            for stream_id in self.stream_ids:
                if account_name == stream_id["account_name"]:
                    stream_ids.append(stream_id)
                    result = True
                    break
        else:
            stream_ids = self.stream_ids

        for stream_id in stream_ids:
            result = True
            with open(stream_id["key_file"], "w+") as key_file:
                key_file.write(stream_id["key"])
                key_file.close()

        return result

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.parent_folder):
            os.mkdir(self.parent_folder)

        if not os.path.exists(self.keys_folder):
            os.mkdir(self.keys_folder)

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
