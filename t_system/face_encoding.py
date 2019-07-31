#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoding
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's encoding human face ability for recognizing them.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import face_recognition
import pickle
import cv2
import os  # Miscellaneous operating system interfaces
import uuid  # The random id generator

from imutils import paths
from shutil import copy, rmtree
from tinydb import TinyDB, Query  # TinyDB is a lightweight document oriented database
from base64 import b64decode
from os import listdir
from os.path import isfile, join
from multipledispatch import dispatch

from t_system import dot_t_system_dir


class FaceEncodeManager:
    """Class to define a face encode manager of tracking system..

        This class provides necessary initiations and a function named
        :func:`t_system.face_encoding.FaceEncodeManager.add_face` for the generating faces to creating encoding pickle file them.
    """

    def __init__(self, detection_method="hog"):
        """Initialization method of :class:`t_system.face_encoding.FaceEncodeManager` class.

        Args:
            detection_method (str):   face detection model
        """
        self.detection_method = detection_method  # either `hog` or `cnn`

        self.recognition_folder = f'{dot_t_system_dir}/recognition'
        self.encodings_folder = f'{self.recognition_folder}/encodings'
        self.dataset_folder = f'{self.recognition_folder}/dataset'
        self.main_encoding_file = f'{self.recognition_folder}/main_encoding.pickle'

        self.check_folders()

        self.db = TinyDB(self.recognition_folder + '/db.json')
        self.table = self.db.table("faces")

        self.face_encoder = FaceEncoder(detection_method)

        self.faces = []
        self.get_existing_faces()

    @dispatch(str, str)
    def add_face(self, name, dataset_folder):
        """The high-level method to create new face using given external dataset.

        Args:
            name (str):           The name of the man who has face in dataset.
            dataset_folder (str):          The path of the dataset that will be encoded.
        """
        face = Face(name)

        src_files = os.listdir(dataset_folder)
        for file_name in src_files:
            full_file_name = os.path.join(dataset_folder, file_name)
            if os.path.isfile(full_file_name):
                copy(full_file_name, face.dataset_folder)

        face.refresh_image_names()

        self.face_encoder.encode(face.dataset_folder, face.pickle_file, face.name)
        self.faces.append(face)

    @dispatch(str, list)
    def add_face(self, name, photos):
        """The high-level method to create new face using base64 encoded photos.

        Args:
            name (str):           The name of the man who has face in dataset.
            photos (list):        The person's raw photo data list. Contains list of {"name": "photo_name", "base_sf": "Base64_encoded_data"}.
        """
        face = Face(name)
        face.create_dataset_from_base_sf_photos(photos)

        self.face_encoder.encode(face.dataset_folder, face.pickle_file, face.name)
        self.faces.append(face)

    def update_face(self, id, photos):
        """The high-level method to update face.

        Args:
            id (str):               The id of the face.
            photos (list):             The person's raw photo data list. Contains list of {"name": "photo_name", "base_sf": "Base64_encoded_data"}.
        """

        for face in self.faces:
            if face.id == id:
                # ELIMINATION OF EXISTING PHOTOS WILL BE HERE
                face.create_dataset_from_base_sf_photos(photos)
                self.face_encoder.encode(face.dataset_folder, face.pickle_file, face.name)
                return True
        return False

    def delete_face(self, id):
        """The high-level method to delete face via given face id.

        Args:
            id (str):               The id of the face.
        """

        for face in self.faces:
            if face.id == id:
                face.remove_self()
                self.faces.remove(face)  # for removing object from list
                return True
        return False

    def get_existing_faces(self):
        """The low-level method to get existing images from the database.
        """
        self.faces.clear()

        faces = self.table.all()

        for face in faces:
            # face = {"id": face_id, "name": face_name, "image_names": []}
            self.faces.append(Face(face["name"], face["id"]))

    def check_folders(self):
        """The low-level method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.recognition_folder):
            os.mkdir(self.recognition_folder)

        if not os.path.exists(self.encodings_folder):
            os.mkdir(self.encodings_folder)

        if not os.path.exists(self.dataset_folder):
            os.mkdir(self.dataset_folder)


class FaceEncoder:
    """Class to define a face encoder of tracking system..

        This class provides necessary initiations and a function named
        :func:`t_system.face_encoder.FaceEncoder.encode` for the generating pickle files with given image dataset and
    """

    def __init__(self, detection_method="hog"):
        """Initialization method of :class:`t_system.face_encoder.FaceEncoder` class.

        Args:
            detection_method (str):   face detection model
        """

        self.detection_method = detection_method  # either `hog` or `cnn`
        self.is_creating_pickle_completed = False

    def encode(self, dataset_folder, pickle_file, face_name=None):
        """The high-level method to generate encoding pickle files from given dataset.

        Args:
            dataset_folder (str):   The path of the dataset that will be encoded.
            pickle_file (str):      The file that is keep faces's encoded data
            face_name (str):        The name of the man who has face in dataset.
        """

        self.is_creating_pickle_completed = False
        print("[INFO] quantifying faces...")  # grab the paths to the input images in our dataset
        image_paths = list(paths.list_images(dataset_folder))

        known_encodings = []
        known_names = []
        name = face_name
        previous_name = ""
        different_name_count = 1

        for (i, image_path) in enumerate(image_paths):

            # extract the person name from the image path
            print(f"[INFO] processing image {i + 1}/{len(image_paths)}")
            if face_name is None:
                name = image_path.split(os.path.sep)[-2]

            if name != previous_name and previous_name:
                different_name_count += 1

                self.write_to_pickle(pickle_file, known_encodings, known_names)

                known_encodings.clear()
                known_names.clear()

            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(rgb, model=self.detection_method)

            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:

                known_encodings.append(encoding)
                known_names.append(name)

            previous_name = name

        if different_name_count == 1:
            self.write_to_pickle(pickle_file, known_encodings, known_names)

        self.is_creating_pickle_completed = True

    def write_to_pickle(self, pickle_file, known_encodings, known_names):
        """The low-level method to writing encodings and names to the given pickle file .

        Args:
            pickle_file (str):          The file that is keep faces's encoded data
            known_encodings (list):     Existing encodings inside the pickle file
            known_names (list):         Existing names inside the pickle file
        """

        existing_encodings, existing_names = self.get_existing_encoding_data(pickle_file)
        known_encodings.extend(existing_encodings)
        known_names.extend(existing_names)

        data = {"encodings": known_encodings, "names": known_names}

        f = open(pickle_file, "wb")
        f.write(pickle.dumps(data))
        f.close()

    @staticmethod
    def generate_main_pickle_file(encodings_folder, main_pickle_file):
        """The low-level method to generate main encoding file from existing face encodings via merging separated encoding pickle files to one.

        Args:
            encodings_folder (str):     The folder that is keep all faces's encoded data files.
            main_pickle_file (str):     The file that is keep merged all faces's encoded data.
        """

        main_decoding = {"encodings": [], "names": []}

        encoding_files = list(paths.list_files(encodings_folder))

        for encoding_file in encoding_files:

            encoding = open(encoding_file, "rb")
            decoding = pickle.load(encoding)

            main_decoding["encodings"].extend(decoding["encodings"])
            main_decoding["names"].extend(decoding["names"])

            encoding.close()

        main_encoding = open(main_pickle_file, "wb")
        main_encoding.write(pickle.dumps(main_decoding))
        main_encoding.close()

    @staticmethod
    def get_existing_encoding_data(pickle_file):
        """The low-level method to get existing encoding data from inside of given pickle file.

        Args:
            pickle_file (str):      The file that is keep faces's encoded data
        """

        if os.path.exists(pickle_file):
            data = pickle.loads(pickle_file)
            return data["encodings"], data["names"]

        return [], []

    def get_completion_status(self):
        """The high-level method to get completion status of face encoding.
        """

        return self.is_creating_pickle_completed


class Face:
    """Class to define a face that has dataset and encoding pickle file.

        This class provides necessary initiations and a function named :func:`t_system.face_encoding.Face.create_dataset_from_base_sf_photos`
        for the provide creating dataset images from the given photos list that is contains photos names and their bas64 encoded form.

    """

    def __init__(self, name, id=None):
        """Initialization method of :class:`t_system.face_encoder.Face` class.

        Args:
            name (str):             The name of the man who has face in dataset.
            id (str):               The id of the face.
        """

        self.name = name
        self.id = id

        self.id = id
        if not id:
            self.id = str(uuid.uuid1())

        self.recognition_folder = f'{dot_t_system_dir}/recognition'
        self.dataset_folder = f'{self.recognition_folder}/dataset/{self.name}'
        self.pickle_file = f'{self.recognition_folder}/encodings/{self.name}_encoding.pickle'

        self.db = TinyDB(self.recognition_folder + '/db.json')
        self.table = self.db.table("faces")

        self.image_names = []
        self.refresh_image_names()

        self.db_upsert()

    def copy_images_to(self, dest):
        """The low-level method to copying image inside the dataset to the giiven destination folder.

        Args:
            dest (str):            Destination folder to copying images those are inside the dataset.
        """

        if not os.path.exists(dest):
            os.mkdir(dest)
        rmtree(dest)

        src_files = os.listdir(self.dataset_folder)
        for file_name in src_files:
            full_file_name = os.path.join(self.dataset_folder, file_name)
            if os.path.isfile(full_file_name):
                copy(full_file_name, dest)

    def db_upsert(self, force_insert=False):
        """Function to insert(or update) the face to the database.

        Args:
            force_insert (bool):    Force insert flag.

        Returns:
            str:  Response.
        """

        if self.table.search((Query().id == self.id)):
            if force_insert:
                # self.already_exist = False
                self.table.update({'name': self.name, 'image_names': self.image_names}, Query().id == self.id)

            else:
                # self.already_exist = True
                return "Already Exist"
        else:
            self.table.insert({
                'id': self.id,
                'name': self.name,
                'image_names': self.image_names
            })  # insert the given data

        return ""

    def refresh_image_names(self, use_db=False):
        """The low-level method to reload the image_names from given source flag.

        Args:
            use_db (bool):      Refreshing source flag. False is for using directly by scanning dataset folder
        """

        if use_db:
            face = self.table.search((Query().id == self.id))

            self.image_names = face["image_names"]
        else:

            self.image_names = [f for f in listdir(self.dataset_folder) if isfile(join(self.dataset_folder, f))]

    def delete_images(self, image_names):
        """The low-level method to deleting images via given image names.

        Args:
            image_names (list):      The name list of the images those inside the dataset.
        """

        for image_name in image_names:
            self.image_names.remove(image_name)
            os.remove(f'{self.dataset_folder}/{image_name}')

        self.db_upsert(force_insert=True)

    def create_dataset_from_base_sf_photos(self, photos):
        """The low-level method to creating image that will be dataset for recognizing person's face later from base64 encoded string photo data.

        Args:
            photos (list):             The person's raw photo data list. Contains list of {"name": "photo_name", "base_sf": "Base64_encoded_data"}.

        Returns:
            str:  dataset.
        """

        for photo in photos:
            with open(f'{self.dataset_folder}/{photo["name"]}.png', "wb") as dataset_image:
                dataset_image.write(b64decode(photo["base_sf"]))

        self.refresh_image_names()
        self.db_upsert(force_insert=True)

    def remove_self(self):
        """The high-level method to remove face itself.
        """

        rmtree(self.dataset_folder)
        os.remove(self.pickle_file)

        self.table.remove((Query().id == self.id))
