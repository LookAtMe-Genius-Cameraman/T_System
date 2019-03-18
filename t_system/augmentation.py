#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: augmentation
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's about communicating with the A.V.A. Augmented ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time

import threading

from t_system.mqtt import MqttReceimitter


class Augmenter():
    """Class to define a take orders ability from remote user of tracking system..

        This class provides necessary initiations and a function named :func:`t_system.Augmenter.run`
        as the loop for checking each incoming messages and :func:`t_system.Augmenter.fulfill`
        as checker for realize the processes to incoming messages.

        """

    def __init__(self, vision):
        """Initialization method of :class:`t_system.Augmenter` class.

        Args:
                vision:       	        Vision object from t_system.vision.Vision Class.

        """
        self.mqtt_receimitter = MqttReceimitter('10.42.0.151')

        mqtt_proc = threading.Thread(target=self.mqtt_receimitter.subscribe, args=('Augmented/T_System',))
        mqtt_proc.start()

        self.vision = vision
        self.vision.set_mqtt_receimitter(self.mqtt_receimitter)

    def run(self):
        """The top-level method to checking incoming message to augmented mode.
        """
        global current_mode
        global current_target

        # Initial value assigning.
        current_mode = ""
        current_target = ""
        workers = []

        while True:
            msg = self.mqtt_receimitter.get_incoming_message()
            if not msg == {}:
                if not msg['options'] == current_mode:
                    if msg['command'] == 'change_mode':
                        stop_thread = True
                        for worker in workers:  # For checking the existing thread.
                            worker.join()
                        workers.clear()
                        stop_thread = False

                        if msg['options'] == 'track':
                            thread = threading.Thread(target=self.vision.detect_track, args=(lambda: stop_thread,))
                            workers.append(thread)
                            thread.start()
                        elif msg['options'] == 'security':
                            thread = threading.Thread(target=self.vision.security, args=(lambda: stop_thread,))
                            workers.append(thread)
                            thread.start()
                        elif msg['options'] == 'learn':
                            thread = threading.Thread(target=self.vision.learn, args=(lambda: stop_thread,))
                            workers.append(thread)
                            thread.start()
                        elif msg['options'] == 'shutdown':
                            # Here is for shutdown the system.
                            pass
                        current_mode = msg['options']

                        self.mqtt_receimitter.publish('T_System/Augmented', {'command': 're-check', 'options': 'realized'})
                elif not msg['options'] == current_target:
                    if msg['command'] == 'change_target':
                        if msg['options'] == ('cat' or 'cats'):
                            self.vision.change_object_cascade("haarcascade_frontalcatface_extended.xml")
                        elif msg['options'] == ('clock' or 'wall clock'):
                            self.vision.change_object_cascade("haarcascade_wallclock.xml")
                        current_target = msg['options']
                        self.mqtt_receimitter.publish('T_System/Augmented', {'command': 're-check', 'options': 'realized'})
                elif msg['options'] == current_mode:
                    self.mqtt_receimitter.publish('T_System/Augmented', {'command': 're-check', 'options': 'already_running'})
                elif msg['options'] == current_target:
                    self.mqtt_receimitter.publish('T_System/Augmented', {'command': 're-check', 'options': 'already_tracking'})
            time.sleep(0.5)








