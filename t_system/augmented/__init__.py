#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __init__
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's about communicating with the A.V.A. Augmented ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import time  # Time access and conversions

import threading

from t_system.augmented.mqtt import MqttReceimitter
from t_system.augmented.online_stream import start_stream

from t_system import seer


class Augmenter:
    """Class to define a take orders ability from remote user of tracking system..

        This class provides necessary initiations and a function named :func:`t_system.augmented.Augmenter.run`
        as the loop for checking each incoming messages and :func:`t_system.augmented.Augmenter.fulfill`
        as checker for realize the processes to incoming messages.

        """

    def __init__(self):
        """Initialization method of :class:`t_system.augmented.Augmenter` class.
        """
        self.mqtt_receimitter = MqttReceimitter('10.42.0.151')

        mqtt_proc = threading.Thread(target=self.mqtt_receimitter.subscribe, args=('Augmented/T_System',))
        mqtt_proc.start()

        seer.__set_mqtt_receimitter(self.mqtt_receimitter)

    def run(self, stop_main_thread):
        """The top-level method to checking incoming message to augmented mode.

        Args:
            stop_main_thread:   	       Stop flag of the tread about terminating it outside of the function's loop.
        """
        global current_mode
        global current_target

        # Initial value assigning.
        current_mode = ""
        current_target = ""
        current_stream_state = ""
        working_mode_threads = []
        working_live_stream_threads = []

        msg_order_report = {'status': False, 'for': '', 'reason': '', 'options': ''}

        while True:
            if stop_main_thread():

                stop_thread = True
                for worker in working_mode_threads:  # For killing the existing thread.
                    worker.join()

                break

            msg = self.mqtt_receimitter.get_incoming_message()
            if not msg == {}:
                if msg['for'] == 'change_mode':
                    if not msg['reason'] == current_mode:
                        stop_thread = True
                        for worker in working_mode_threads:  # For checking the existing thread.
                            worker.join()
                        working_mode_threads.clear()
                        stop_thread = False

                        watch_thread = threading.Thread(target=seer.watch, args=(lambda: stop_thread, "bgr", msg['reason']))
                        working_mode_threads.append(watch_thread)
                        watch_thread.start()

                        if msg['reason'] == 'track':
                            track_thread = threading.Thread(target=seer.detect_track, args=(lambda: stop_thread,))
                            working_mode_threads.append(track_thread)
                            track_thread.start()
                        elif msg['reason'] == 'security':
                            secure_thread = threading.Thread(target=seer.scan, args=(lambda: stop_thread, 3))
                            working_mode_threads.append(secure_thread)
                            secure_thread.start()
                        elif msg['reason'] == 'learn':
                            learn_thread = threading.Thread(target=seer.learn, args=(lambda: stop_thread,))
                            working_mode_threads.append(learn_thread)
                            learn_thread.start()
                        elif msg['reason'] == 'shutdown':
                            # Here is for shutdown the system.
                            pass
                        current_mode = msg['reason']
                        msg_order_report['status'] = True
                    else:
                        msg_order_report['status'] = False
                        msg_order_report['options'] = 'already'

                    msg_order_report['for'] = 'change_mode'
                    msg_order_report['reason'] = msg['reason']

                elif msg['for'] == 'change_target':
                    if not msg['reason'] == current_target:
                        if msg['reason'] == ('cat' or 'cats'):
                            seer.change_tracked_thing("frontalcatface_extended")
                        elif msg['reason'] == ('clock' or 'wall clock'):
                            seer.change_tracked_thing("wallclock")

                        current_target = msg['reason']
                        msg_order_report['status'] = True
                    else:
                        msg_order_report['status'] = False
                        msg_order_report['options'] = 'already'

                    msg_order_report['for'] = 'change_target'
                    msg_order_report['reason'] = msg['reason']

                elif msg['for'] == 'live_stream':
                    if not msg['reason'] == current_stream_state:
                        if msg['reason'] == 'start':
                            track_thread = threading.Thread(target=start_stream, args=(lambda: stop_thread, seer.camera))
                            working_live_stream_threads.append(track_thread)
                            track_thread.start()
                        if msg['reason'] == 'stop':
                            stop_thread = True
                            for worker in working_live_stream_threads:  # For checking the existing thread.
                                worker.join()
                            working_mode_threads.clear()
                            stop_thread = False

                        current_stream_state = msg['reason']
                        msg_order_report['status'] = True
                        msg_order_report['options'] = '10.42.0.151:8000'

                    else:
                        msg_order_report['status'] = False
                        msg_order_report['options'] = 'already'

                    msg_order_report['for'] = 'live_stream'
                    msg_order_report['reason'] = msg['reason']
                self.mqtt_receimitter.publish('Augmented/A.V.A.', msg_order_report)

            time.sleep(0.5)
