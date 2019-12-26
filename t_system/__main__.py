#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: __main__
    :platform: Unix
    :synopsis: the top-level module of T_System that contains the entry point and handles built-in commands.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import argparse
import os
import sys

from elevate import elevate

from t_system.logging import LogManager

import t_system.__init__
from t_system import dot_t_system_dir

logger = None


def start(args):
    """Function that starts the tracking system with the correct mode according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """
    from t_system.vision import Vision

    t_system.seer = Vision(args)

    try:
        if args["interface"] == "official_stand":

            from t_system.stand import Stand

            t_system.stand_ui = Stand(args)
            t_system.stand_ui.run()

        elif args["interface"] == "augmented":
            from t_system.augmented import Augmenter

            t_system.augmenter = Augmenter()
            t_system.augmenter.run(lambda: False)

        elif args["interface"] == "remote_ui":
            from t_system.remote_ui.__main__ import RemoteUI

            remote_ui = RemoteUI(args)
            remote_ui.run(host=args["host"], port=args["port"], debug=args["debug"])

        else:
            if args["learn"]:
                t_system.seer.watch_and("learn")
            elif args["security"]:
                t_system.seer.watch_and("secure")
            else:
                t_system.seer.watch_and("track")

    except KeyboardInterrupt:
        logger.debug("Vision systems has been released!")
        t_system.seer.release_members()


def start_sub(args):
    """Function that starts the tracking system with the sub jobs according to command-line arguments.

    Args:
        args:       Command-line arguments.
    """

    if args["sub_jobs"] == "id":

        if args["id_sub_jobs"] == "set":
            t_system.identifier.change_keys(args["public_id"], args["private_id"], args["name"])
        elif args["id_sub_jobs"] == "show":
            t_system.identifier.show_keys()

    elif args["sub_jobs"] == "remote-ui-authentication":
        t_system.administrator.change_keys(args["ssid"], args["password"])

    elif args["sub_jobs"] == "encode-face":
        from t_system.face_encoding import FaceEncodeManager

        face_encode_manager = FaceEncodeManager(args["detection_method"])
        face_encode_manager.add_face(args["owner_name"], args["dataset"])

    elif args["sub_jobs"] == "self-update":

        t_system.update_manager.set_editability(args["editable"])
        t_system.update_manager.set_verbosity(args["verbose"])
        t_system.update_manager.update()

    elif args["sub_jobs"] == "arm":

        from t_system.motion.arm.modelisation import ArmModeler

        if args["arm_sub_jobs"] == "create":
            ArmModeler().create(args["name"])
        elif args["arm_sub_jobs"] == "list":
            ArmModeler().show(args["name"])

    elif args["sub_jobs"] == "live-stream":

        from t_system.online_stream import OnlineStreamer

        online_streamer = OnlineStreamer(None, None)

        if args["live_st_sub_jobs"] == "website":
            if args["live_st_website_sub_jobs"] == "upsert":
                online_streamer.add_website(args["name"], args["url"], args["server"], force_insert=True)

            elif args["live_st_website_sub_jobs"] == "remove":
                online_streamer.remove_websites(args["website_ids"])

            elif args["live_st_website_sub_jobs"] == "list":
                online_streamer.show_websites()

        elif args["arm_sub_jobs"] == "streaming":
            if args["live_st_streaming_sub_jobs"] == "upsert":
                online_streamer.set_website_stream(args["website_id"], {"account_name": args["account_name"], "key": args["key"]})

            elif args["live_st_streaming_sub_jobs"] == "remove":
                online_streamer.remove_website_stream(args["website_id"], args["account_name"])

            elif args["live_st_streaming_sub_jobs"] == "list":
                online_streamer.show_stream_ids()

    elif args["sub_jobs"] == "r-sync":

        if args["list-services"]:
            t_system.r_synchronizer.show_services()

        elif args["r_sync_sub_jobs"] == "sync":
            t_system.r_synchronizer.start_sync(args["service_name"], args["name"])

        elif args["r_sync_sub_jobs"] == "account":

            if args["r_sync_account_sub_jobs"] == "upsert":
                t_system.r_synchronizer.set_service_account(args["service_name"], {"name": args["name"], "key": args["key"]})

            elif args["r_sync_account_sub_jobs"] == "remove":
                pass
                t_system.r_synchronizer.remove_service_account(args["service_name"], args["name"])

            elif args["r_sync_account_sub_jobs"] == "list":
                t_system.r_synchronizer.show_accounts()


def prepare(args):
    """The function that prepares the working environment for storing data during running.

    Args:
        args:       Command-line arguments.
    """

    if args["interface"] == "official_stand" or args["interface"] == "remote_ui":
        elevate(show_console=False, graphical=False)

    if not os.path.exists(dot_t_system_dir):
        os.mkdir(dot_t_system_dir)

    from t_system.presentation import startup_banner
    startup_banner()

    t_system.log_manager = LogManager(args)

    global logger
    logger = t_system.log_manager.get_logger(__name__, "DEBUG")
    logger.info("Logger integration successful.")

    if args["ext_servo_driver"]:
        from adafruit_servokit import ServoKit
        t_system.motor_driver = ServoKit(channels=args["sd_channels"])
        logger.info("Motors running on external driver.")

    from t_system.accession import NetworkConnector
    from t_system.administration import Identifier
    from t_system.administration import Administrator
    from t_system.updation import UpdateManager
    from t_system.motion.arm import Arm
    from t_system.motion.action import MissionManager
    from t_system.recordation import RecordManager
    from t_system.face_encoding import FaceEncodeManager
    from t_system.r_synchronization import RSynchronizer

    t_system.network_connector = NetworkConnector(args)
    t_system.identifier = Identifier()
    t_system.administrator = Administrator()
    t_system.update_manager = UpdateManager()
    t_system.arm = Arm(args["arm_name"], args["ext_servo_driver"])
    t_system.mission_manager = MissionManager()
    t_system.record_manager = RecordManager()
    t_system.face_encode_manager = FaceEncodeManager()
    t_system.r_synchronizer = RSynchronizer()

    if not args["no_emotion"]:
        from t_system.motion.action import EmotionManager
        t_system.emotion_manager = EmotionManager()

    if args["sub_jobs"]:
        start_sub(args)
        sys.exit(1)

    if args["access_point"]:
        from t_system.accession import AccessPoint

        elevate(show_console=False, graphical=False)

        access_point = AccessPoint(args)
        access_point.start()

    if not args["AI"] or args["non_moving_target"]:
        if args["learn"]:
            raise Exception('All AI learning tools deprecated. Don\'t use the learn mode without AI.')

    logger.info("Package preparation completed.")


def initiate():
    """The top-level method to serve as the entry point of T_System.

    This method is the entry point defined in `setup.py` for the `t_system` executable that placed a directory in `$PATH`.

    This method parses the command-line arguments and handles the top-level initiations accordingly.
    """

    ap = argparse.ArgumentParser()

    w_mode_gr = ap.add_argument_group('user-interfaces')
    w_mode_gr.add_argument("--interface", help="Set the user interfaces. To use: either `official_stand`, `augmented`, `remote_ui` or None."
                                               "`official_stand`: for using the interface of official T_System stand."
                                               "`augmented`: Augmented control with the Augmented Virtual Assistant A.V.A.. \'https://github.com/MCYBA/A.V.A.\' is the home page of the A.V.A. and usage explained into the \'AUGMENTED.md\'."
                                               "`remote_ui`: remote control with created graphic interface that is power by flask available on desktop or mobile."
                                               "None: Use to just by `running modes` parameters."
                                               "The default value is None.", action="store", type=str, choices=["official_stand", "augmented", "remote_ui", None], default=None)

    official_stand_gr = ap.add_argument_group('official_stand')
    official_stand_gr.add_argument("--stand-gpios", help="GPIO pin numbers of official stand's LEDs and fans. 5(as red led), 6(as green led) and 14(as fan) GPIO pins are default.", nargs=3, default=[5, 6, 14], type=int, metavar=('RED-LED', 'GREEN-LED', 'FAN'))

    remote_ui_gr = ap.add_argument_group('remote_ui')
    remote_ui_gr.add_argument("--host", help="Specify host address.", action="store", type=str, default="0.0.0.0")
    remote_ui_gr.add_argument("--port", help="Specify the port.", action="store", type=str, default="5000")
    remote_ui_gr.add_argument("--debug", help="Activate debug mode.", action="store_true")

    r_mode_gr = ap.add_argument_group('Running Modes')
    r_mode_gr.add_argument("-l", "--learn", help="Teach Mode. Teach the object tracking parameters with the trial and error method.", action="store_true")
    r_mode_gr.add_argument("-s", "--security", help="Security Mode. Scan the around and optionally take photos of visitors.", action="store_true")

    tool_gr = ap.add_argument_group('Running Tools')
    tool_gr.add_argument("--detection-model", help="Object detection model to use: either `haarcascade`, `hog` or `cnn`. `hog` and `cnn` can only use for detecting human faces. `haarcascade` is default.", action="store", type=str, default="haarcascade")
    tool_gr.add_argument("--cascades", help="Specify the trained detection algorithm file for the object detection ability. Sample: 'frontalface_default' for frontalface_default.xml file under the 'haarcascade' folder.", action="store", type=list, default=["frontalface_default", "profileface"])
    tool_gr.add_argument("-j", "--no-recognize", help="Do not recognize the things.(faces, objects etc.)", action="store_true")
    tool_gr.add_argument("--encoding-file", help="Specify the trained recognition encoding pickle file for recognize object. Sample: 'jane_encoding' for jane_encoding.pickle file under the '.t_system/recognition/encodings' folder in your Home directory. "
                                                 "If `main_encoding` chosen, `main_encoding.pickle` file that creates from merging all encoding files under `.../encodings` folder will used. Default is `main_encoding`", action="store", type=str, default="main_encoding")
    tool_gr.add_argument("--use-tracking-api", help="Use the openCV's tracking API for realize the next object is same as previous one.", action="store_true")
    tool_gr.add_argument("--tracker-type", help="OpenCV's tracking type to use: either `BOOSTING`, `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE` or `CSRT`. `CSRT` is default.", action="store", type=str, choices=["BOOSTING", "MIL", "KCF", "TLD", "MEDIANFLOW", "GOTURN", "MOSSE", "CSRT"], default="CSRT")

    camera_gr = ap.add_argument_group('Camera Options')
    camera_gr.add_argument("--camera-rotation", help="Specify the camera's ratational position. 180 degree is default.", action="store", default=180, type=int)
    camera_gr.add_argument("--resolution", help="Specify the camera's resolution of vision ability. 320x240 is default", nargs=2, default=[80, 60], type=int, metavar=('WIDTH', 'HEIGHT'))

    shoot_gr = ap.add_argument_group('Shoot Options')
    shoot_gr.add_argument("--framerate", help="Specify the camera's framerate. of vision ability. 32 fps is default.", action="store", default=32, type=int)
    shoot_gr.add_argument("--chunk", help="Smallest unit of audio. 1024*8=8192 bytes are default.", action="store", default=8192, type=int)
    shoot_gr.add_argument("--rate", help="Bit Rate of audio stream / Frame Rate. 44100 Hz sample rate is default.", action="store", default=44100, type=int)
    shoot_gr.add_argument("--channels", help="Number of microphone's channels. Default value is 1.", action="store", default=1, type=int)
    shoot_gr.add_argument("--audio_device_index", help="Index of the using audio device. 2 is default.", action="store", default=2, type=int)
    shoot_gr.add_argument("--shoot-formats", help="Formats for recording the work. `h264` and `wav` for separate video and audio recording and `mp4` for merged file are default.", nargs=3, default=["h264", "wav", "mp4"], type=str, metavar=('VIDEO', 'AUDIO', 'MERGED'))

    shot_gr = ap.add_argument_group('Shot Options')
    shot_gr.add_argument("--shot-format", help="Format for take shots. `jpg` is default", default="jpg", type=str, metavar=('SHOT',))

    motion_gr = ap.add_argument_group('Motion Mechanism')
    motion_gr.add_argument("-x", "--ext-servo-driver", help="Use external servo motor driver board.", action="store_true")
    motion_gr.add_argument("--sd-channels", help="Number of external servo driver's channels. Default value is 16.", action="store", default=16, type=int)

    robotic_arm_gr = ap.add_argument_group('Robotic Arm')
    robotic_arm_gr.add_argument("--arm-name", help="One of the robotic arm names those are defined in config.json file. The arm is for relocating the 2 axis target locking system hybrid-synchronously.", default="Senior", type=str, metavar=('ARM',))

    lock_sys_gr = motion_gr.add_argument_group('Target Locking System')
    lock_sys_gr.add_argument("--ls-gpios", help="GPIO pin numbers of the 2 axis target locking system's servo motors. 23(as pan) and 24(as tilt) GPIO pins are default.", nargs=2, default=[23, 24], type=int, metavar=('PAN', 'TILT'))
    lock_sys_gr.add_argument("--ls-channels", help="Servo driver channels of the 2 axis target locking system's servo motors. 4(as pan) and 3(as tilt) channels are default.", nargs=2, default=[4, 3], type=int, metavar=('PAN', 'TILT'))
    lock_sys_usage_gr = lock_sys_gr.add_mutually_exclusive_group()
    lock_sys_usage_gr.add_argument("--AI", help="Specify the learning method of how to move to the target position from the current. When the nothing chosen, learn mode and decision mechanisms will be deprecated. to use: either `official_ai`", action="store", type=str, default=None)
    lock_sys_usage_gr.add_argument("--non-moving-target", help="Track the non-moving objects. Don't use AI or OpenCv's object detection methods. Just try to stay focused on the current focus point with changing axis angles by own position.", action="store_true")
    lock_sys_usage_gr.add_argument("--arm-expansion", help="Use the Target Locking System as the extension of the Robotic Arm. Don't use AI or OpenCv's object detection methods. Add 2 more joints to the Robotic Arm", action="store_true")

    access_p_gr = ap.add_argument_group('Access Point Options')
    access_p_gr.add_argument("-p", "--access-point", help="Become access point for serving remote UI inside the internal network.", action="store_true")
    access_p_gr.add_argument("--ap-wlan", help="Network interface that will be used to create HotSpot. 'wlan0' is default.", action="store", default="wlan0", type=str)
    access_p_gr.add_argument("--ap-inet", help="Forwarding interface. Default is None.", action="store", default=None, type=str)
    access_p_gr.add_argument("--ap-ip", help="Ip address of this machine in new network. 192.168.45.1 is default.", action="store", default="192.168.45.1", type=str)
    access_p_gr.add_argument("--ap-netmask", help="Access Point netmask address. 255.255.255.0 is default.", action="store", default="255.255.255.0", type=str)
    access_p_gr.add_argument("--ssid", help="Preferred access point name. 'T_System' is default.", action="store", default="T_System", type=str)
    access_p_gr.add_argument("--password", help="Password of the access point. 't_system' is default.", action="store", default="t_system", type=str)

    ext_network_gr = ap.add_argument_group('External Network Options')
    ext_network_gr.add_argument("--wlan", help="network interface that will be used to connect to external network. 'wlan0' is default.", action="store", default="wlan0", type=str)
    ext_network_gr.add_argument("--inet", help="Forwarding interface. Default is None.", action="store", default=None, type=str)
    ext_network_gr.add_argument("--static-ip", help="The static IP address for the connected external network, if wanted. ", action="store", type=str)
    ext_network_gr.add_argument("--netmask", help="Netmask address. 255.255.255.0 is default.", action="store", default="255.255.255.0", type=str)
    ext_network_gr.add_argument("--country-code", help="Wifi country code for the wpa_supplicant.conf. To use look at: https://github.com/recalbox/recalbox-os/wiki/Wifi-country-code-(EN). Default is `TR`", action="store", default="TR", type=str)

    other_gr = ap.add_argument_group('Others')
    other_gr.add_argument("--environment", help="The running environment. It specify the configuration files and logs. To use: either `production`, `development` or `testing`. Default is production", action="store", type=str,  choices=["production", "development", "testing"], default="development")
    other_gr.add_argument("--no-emotion", help="Do not mak feelings with using motion mechanisms.(Arm and Locking System.)", action="store_true")
    other_gr.add_argument("-S", "--show-stream", help="Display the camera stream. Enable the stream window.(Require gui environment.)", action="store_true")
    other_gr.add_argument("-m", "--found-object-mark", help="Specify the mark type of the found object.  To use: either `single_rect`, `rotating_arcs`, `partial_rect` or None. Default is `single_rect`", action="store", choices=["single_rect", "rotating_arcs", "partial_rect", "animation_1", None], default="single_rect", type=str)
    other_gr.add_argument("-r", "--record", help="Record the video stream. Files are named by the date.", action="store_true")
    other_gr.add_argument("-v", "--verbose", help="Print various debugging logs to console for debug problems", action="store_true")
    other_gr.add_argument("--version", help="Display the version number of T_System.", action="store_true")

    sub_p = ap.add_subparsers(dest="sub_jobs", help='officiate the sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_id = sub_p.add_parser('id', help='Make identification jobs of T_System.')
    id_sub_p = ap_id.add_subparsers(dest="id_sub_jobs", help='officiate the identification sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_id_set = id_sub_p.add_parser('set', help='Setting the identity of T_System for detecting specific working device of it.')
    ap_id_set.add_argument('--public_id', help='Specific and unique ID of T_System.', type=str)
    ap_id_set.add_argument('--private_id', help='Specific and unique ID of T_System.', type=str)
    ap_id_set.add_argument('--name', help='Specific name for T_System.', type=str)

    ap_id_show = id_sub_p.add_parser('show', help='Getting the identity info of T_System.')

    ap_r_ui_auth = sub_p.add_parser('remote-ui-authentication', help='Remote UI administrator authority settings of the secret entry point that is the new network connection panel.')
    ap_r_ui_auth.add_argument('--ssid', help='Secret administrator ssid flag', type=str)
    ap_r_ui_auth.add_argument('--password', help='Secret administrator password flag', type=str)

    ap_face_encode = sub_p.add_parser('encode-face', help='Generate encoded data from the dataset folder to recognize the man T_System is monitoring during operation.')
    ap_face_encode.add_argument("-i", "--dataset", help="Path to input directory of faces + images.", required=True)
    ap_face_encode.add_argument("-n", "--owner-name", help="Name of the images owner. If there is single man who has the images, give the name of that man with dataset", type=str, default=None)
    ap_face_encode.add_argument("-d", "--detection-method", help="Face detection model to use: either `hog` or `cnn` default is `hog`", type=str, default="hog")

    ap_self_update = sub_p.add_parser('self-update', help='Update source code of t_system itself via `git pull` command from the remote git repo.')
    ap_self_update.add_argument("-e", "--editable", help="Update the T_System in editable mode (i.e. setuptools'develop mode')", action="store_true")

    ap_arm = sub_p.add_parser('arm', help='Management jobs of Denavit-Hartenberg transform matrix models of robotic arms of T_System.')
    arm_sub_p = ap_arm.add_subparsers(dest="arm_sub_jobs", help='officiate the identification sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_arm_create = arm_sub_p.add_parser('create', help='Create the D-H transform matrix model of given robotic arm name via configuration file.')
    ap_arm_create.add_argument('--name', help='The name of robotic arm in arm module\'s config.json file.', type=str, required=True)

    ap_arm_list = arm_sub_p.add_parser('list', help='List the robotic arms with their model and features')
    ap_arm_list.add_argument('--name', help='The name of robotic arm in arm module\'s config.json file.', type=str, default=None)

    ap_live_st = sub_p.add_parser('live-stream', help='Make Online Stream jobs of T_System.')
    live_st_sub_p = ap_live_st.add_subparsers(dest="live_st_sub_jobs", help='officiate the Online Stream sub-jobs')  # if sub-commands not used their arguments create raise.

    ap_live_st_website = live_st_sub_p.add_parser('website', help='Make jobs about Live Streaming available websites.')
    l_s_website_sub_p = ap_live_st_website.add_subparsers(dest="live_st_website_sub_jobs", help='officiate the Online Stream\'s sub-jobs about its websites')  # if sub-commands not used their arguments create raise.

    ap_l_s_website_upsert = l_s_website_sub_p.add_parser('upsert', help='Insert new website for the live streaming point. If name of given website is exist, update its other parameters.')
    ap_l_s_website_upsert.add_argument('--name', help='Name of the website.', type=str, required=True)
    ap_l_s_website_upsert.add_argument('--url', help='Active Internet Link of the website.', type=str, required=True)
    ap_l_s_website_upsert.add_argument('--server', help='Server rtmp Link of the website.', type=str, required=True)

    ap_l_s_website_remove = l_s_website_sub_p.add_parser('remove', help='Remove existing online websites by their name.')
    ap_l_s_website_remove.add_argument('--website-ids', help='ID list of websites that will remove.', type=list, required=True)

    ap_l_s_website_list = l_s_website_sub_p.add_parser('list', help='List the existing websites.')

    ap_live_st_streaming = live_st_sub_p.add_parser('streaming', help='Make jobs about online streaming runtime specifications and parameters')
    l_s_streaming_sub_p = ap_live_st_streaming.add_subparsers(dest="live_st_streaming_sub_jobs", help='officiate the Online Stream\' sub-jobs about its streaming specifications')  # if sub-commands not used their arguments create raise.

    ap_l_s_streaming_upsert = l_s_streaming_sub_p.add_parser('upsert', help='Insert new stream ID for the live streaming point. If name of given ID is exist, update its other parameters.')
    ap_l_s_streaming_upsert.add_argument('--website-id', help='ID of the website that has stream IDs.', type=str, required=True)
    ap_l_s_streaming_upsert.add_argument('--account-name', help='Name of the website personalized account.', type=str, required=True)
    ap_l_s_streaming_upsert.add_argument('--key', help='Stream key of the account', type=str, required=True)

    ap_l_s_streaming_remove = l_s_streaming_sub_p.add_parser('remove', help='Remove a stream ID for the live streaming point.')
    ap_l_s_streaming_remove.add_argument('--website-id', help='ID of the website that has stream IDs.', type=str, required=True)
    ap_l_s_streaming_remove.add_argument('--account-name', help='Name of the personalized account of a website that will be removed.', type=str, required=True)

    ap_l_s_streaming_list = l_s_streaming_sub_p.add_parser('list', help='List the existing websites.')

    ap_r_sync = sub_p.add_parser('r-sync', help='Make remote synchronization jobs of T_System.')
    ap_r_sync.add_argument('--list-services', help='List the remote storage services information.', action="store_true")

    r_sync_sub_p = ap_r_sync.add_subparsers(dest="r_sync_sub_jobs", help='officiate the Remote Synchronization sub-jobs')

    ap_r_sync_sync = r_sync_sub_p.add_parser('sync', help='Make jobs about synchronization recorded videos folder with remote storage service.')
    ap_r_sync_sync.add_argument('--service-name', help='Name of the remote storage service that has accounts. to use: either, `Dropbox`', type=str, choices=["Dropbox"], required=True)
    ap_r_sync_sync.add_argument('--name', help='Name of the personalized account of remote storage service.', type=str, required=True)

    ap_r_snc_acc = r_sync_sub_p.add_parser('account', help='Make jobs about remote storage service accounts.')
    r_sync_acc_sub_p = ap_r_snc_acc.add_subparsers(dest="r_sync_account_sub_jobs", help='officiate the remote storage synchronization\'s sub-jobs about its account specifications')

    ap_r_sync_acc_upsert = r_sync_acc_sub_p.add_parser('upsert', help='Insert new account for specified remote storage service. If name of given account is exist, update its other parameters.')
    ap_r_sync_acc_upsert.add_argument('--service-name', help='Name of the remote storage service that has accounts. to use: either, `Dropbox`', type=str, choices=["Dropbox"], required=True)
    ap_r_sync_acc_upsert.add_argument('--name', help='Name of the personalized account of remote storage service.', type=str, required=True)
    ap_r_sync_acc_upsert.add_argument('--key', help='Stream key of the account', type=str, required=True)

    ap_r_sync_acc_remove = r_sync_acc_sub_p.add_parser('remove', help='Remove existing account about storage services by their name.')
    ap_r_sync_acc_remove.add_argument('--service-name', help='Name of the remote storage service that has accounts. to use: either, `Dropbox`', type=str, choices=["Dropbox"], required=True)
    ap_r_sync_acc_remove.add_argument('--name', help='Name of the personalized account of remote storage service.', type=str, required=True)

    ap_r_sync_acc_list = r_sync_acc_sub_p.add_parser('list', help='List the existing remote storage services.')

    args = vars(ap.parse_args())

    if args["version"]:
        from t_system.presentation import versions_banner
        versions_banner()
        sys.exit(1)

    prepare(args)
    start(args)


if __name__ == '__main__':
    initiate()
