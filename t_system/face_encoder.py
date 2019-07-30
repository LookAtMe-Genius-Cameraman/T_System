#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: face_encoder
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's encoding human face ability for recognition them.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import face_recognition
import pickle
import cv2
import os  # Miscellaneous operating system interfaces

from imutils import paths

from t_system import dot_t_system_dir


class FaceEncoder:
    """Class to define a face encoder of tracking system..

        This class provides necessary initiations and a function named
        :func:`t_system.face_encoder.FaceEncoder.encode`
        for the generating pickle files with encoded data.

    """

    def __init__(self, dataset_folder, detection_method="hog"):
        """Initialization method of :class:`t_system.face_encoder.FaceEncoder` class.

        Args:
            dataset_folder (str):   The path of the dataset that will be encoded.
            detection_method (str):   face detection model
        """
        self.dataset_folder = dataset_folder
        self.detection_method = detection_method  # either `hog` or `cnn`

        self.encodings_folder = dot_t_system_dir + "/recognition_encodings"

        self.is_creating_pickle_completed = False

    def encode(self):
        """Function to insert(or update) the event to the database.

        Returns:
                str:  Response.
        """

        self.is_creating_pickle_completed = False
        print("[INFO] quantifying faces...")  # grab the paths to the input images in our dataset
        image_paths = list(paths.list_images(self.dataset_folder))

        # initialize the list of known encodings and known names
        known_encodings = []
        known_names = []

        # loop over the image paths
        for (i, imagePath) in enumerate(image_paths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1, len(image_paths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from BGR (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb, model=self.detection_method)

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                known_encodings.append(encoding)
                known_names.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": known_encodings, "names": known_names}

        pickle_file = self.get_pickle_file()
        f = open(pickle_file, "wb")
        f.write(pickle.dumps(data))
        f.close()

        self.is_creating_pickle_completed = True

    def get_pickle_file(self):
        """The low-level method to get pickle file existing pickle file count.
        """
        existing_pickle_file_count = len(list(paths.list_files(self.encodings_folder)))
        return self.encodings_folder + "encoding_" + str(existing_pickle_file_count) + ".pickle"

    def get_completion_status(self):
        """The high-level method to get completion status of face encoding.
        """

        return self.is_creating_pickle_completed
