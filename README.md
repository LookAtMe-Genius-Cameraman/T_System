# T_System

the (non-)moving objects tracking system via two axis camera motion (and as optionally n joint robotic arm) for raspberry pi distributions

[![Pyup shield](https://pyup.io/repos/github/connected-life/T_System/shield.svg?label=pyup&color=brightgreen)](https://pyup.io/repos/github/connected-life/T_System/)
[![Pyup python-3 shield](https://pyup.io/repos/github/connected-life/T_System/python-3-shield.svg?label=python%203&color=brightgreen)](https://pyup.io/repos/github/connected-life/T_System/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](code-of-conduct.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/release-pre/connected-life/T_System)](https://github.com/connected-life/T_System)
[![Travis](https://api.travis-ci.org/connected-life/T_System.svg?branch=master)](https://travis-ci.org/connected-life/T_System)
[![Read The Docs](https://readthedocs.org/projects/t-system/badge/?version=latest)](https://t-system.readthedocs.io/en/latest/?badge=latest)
[![Coveralls](https://coveralls.io/repos/github/connected-life/T_System/badge.svg)](https://coveralls.io/github/connected-life/T_System/)
[![Contributors](https://img.shields.io/github/contributors/connected-life/T_System)](https://github.com/connected-life/T_System/graphs/contributors)

![T_System](https://raw.githubusercontent.com/MCYBA/T_System/master/docs/img/on_work.gif)

<br>


#### Supported Environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | Raspbian                                |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
|                         |                                         |

### Requirements

##### Hardware
  
- Raspberry Pi 2,3 B, B + or higher
- Raspberry Pi Camera
- n servo motors
- 2 axis as pan-tilt motions for t_system's locking target ability
- n-2 axis for t_system's robotic arm feature (Optional)

##### Software

- OpenCV. Install via [here](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) or any other place you want.
- Dlib and face_recognition module via [here](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65) or any other place you want.

### Installation

Clone the GitHub repository and run

```Shell
sudo ./install.sh
```

in the repository directory.

for development mode: `sudo ./install-dev.sh`


<sup><i>If there is a failure try `sudo -H ./install-dev.sh`</i></sup>

### Usage <a href="https://t-system.readthedocs.io/en/latest/t_system.html"><img src="https://media.readthedocs.com/corporate/img/header-logo.png" align="right" height="25px" /></a>


```
usage: t_system [-h] [--stand-gpios BUTTON RED-LED GREEN-LED] [--host HOST]
                [--port PORT] [--debug] [-l] [-s]
                [--detection-model DETECTION_MODEL]
                [--cascade-file CASCADE_FILE] [-j]
                [--encoding-file ENCODING_FILE] [--use-tracking-api]
                [--tracker-type TRACKER_TYPE] [--resolution WIDTH HEIGHT]
                [--framerate FRAMERATE] [--chunk CHUNK] [--rate RATE]
                [--channels CHANNELS]
                [--audio_device_index AUDIO_DEVICE_INDEX] [--robotic-arm ARM]
                [--ls-gpios PAN TILT] [--AI AI | --non-moving-target] [-p]
                [--ap-wlan AP_WLAN] [--ap-inet AP_INET] [--ap-ip AP_IP]
                [--ap-netmask AP_NETMASK] [--ssid SSID] [--password PASSWORD]
                [--wlan WLAN] [--inet INET] [--static-ip STATIC_IP]
                [--netmask NETMASK] [-S] [-m FOUND_OBJECT_MARK] [-r]
                [--version]
                interface {remote-ui-authentication,face-encoding,self-update}
                ...

positional arguments:
  {remote-ui-authentication,face-encoding,self-update}
                        officiate the sub-jobs
    remote-ui-authentication
                        remote UI administrator authority settings of the
                        secret entry point that is the new network connection
                        panel.
    face-encoding       generate encoded data from the dataset folder to
                        recognize the man T_System is monitoring during
                        operation.
    self-update         update source code of t_system itself via `git pull`
                        command from the remote git repo.

optional arguments:
  -h, --help            show this help message and exit

user-interfaces:
  interface             Set the user interfaces. To use: either
                        `official_stand`, `augmented`, `remote_ui` or
                        None.`official_stand`: for using the interface of
                        official T_System stand.`augmented`: Augmented control
                        with the Augmented Virtual Assistant A.V.A..
                        'https://github.com/MCYBA/A.V.A.' is the home page of
                        the A.V.A. and usage explained into the
                        'AUGMENTED.md'.`remote_ui`: remote control with
                        created graphic interface that is power by flask
                        available on desktop or mobile.None: Use to just by
                        `running modes` parameters.The default value is None.

official_stand:
  --stand-gpios BUTTON RED-LED GREEN-LED
                        GPIO pin numbers of official stand's the button and
                        the led. 5(as button), 27(as red led) and 22(as green
                        led) GPIO pins are default.

remote_ui:
  --host HOST           Specify host address.
  --port PORT           Specify the port.
  --debug               Activate debug mode.

running modes:
  -l, --learn           Teach Mode. Teach the object tracking parameters with
                        the trial and error method.
  -s, --security        Security Mode. Scan the around and optionally take
                        photos of visitors.

running tools:
  --detection-model DETECTION_MODEL
                        Object detection model to use: either `haarcascade`,
                        `hog` or `cnn`. `hog` and `cnn` can only use for
                        detecting human faces. `haarcascade` is default.
  --cascade-file CASCADE_FILE
                        Specify the trained detection algorithm file for the
                        object detection ability. Sample:
                        'frontalface_default' for frontalface_default.xml file
                        under the 'haarcascade' folder.
  -j, --no-recognize    Do not recognize the things.(faces, objects etc.)
  --encoding-file ENCODING_FILE
                        Specify the trained recognition encoding pickle file
                        for recognize object. Sample: 'encodings' for
                        encodings.pickle file under the
                        'recognition_encodings' folder.
  --use-tracking-api    Use the openCV's tracking API for realize the next
                        object is same as previous one.
  --tracker-type TRACKER_TYPE
                        OpenCV's tracking type to use: either `BOOSTING`,
                        `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE`
                        or `CSRT`. `CSRT` is default.

video options:
  --resolution WIDTH HEIGHT
                        Specify the camera's resolution of vision ability.
                        320x240 is default
  --framerate FRAMERATE
                        Specify the camera's framerate. of vision ability. 32
                        fps is default.
  --chunk CHUNK         Smallest unit of audio. 1024*8=8192 bytes are default.
  --rate RATE           Bit Rate of audio stream / Frame Rate. 44100 Hz sample
                        rate is default.
  --channels CHANNELS   Number of microphone's channels. Default value is 1.
  --audio_device_index AUDIO_DEVICE_INDEX
                        Index of the using audio device. 2 is default.

motion mechanism:
  --robotic-arm ARM     One of the robotic arm names those are defined in
                        arm_config.json file. The arm is for relocating the 2
                        axis target locking system hybrid-synchronously.

target locking system:
  --ls-gpios PAN TILT   GPIO pin numbers of the 2 axis target locking system's
                        servo motors. 23(as pan) and 24(as tilt) GPIO pins are
                        default.
  --AI AI               Specify the learning method of how to move to the
                        target position from the current. When the nothing
                        chosen, learn mode and decision mechanisms will be
                        deprecated. to use: either `official_ai`
  --non-moving-target   Track the non-moving objects. Don't use AI or OpenCv's
                        object detection methods. Just try to stay focused on
                        the current focus point with changing axis angles by
                        own position.

access point options:
  -p, --access-point    Become access point for serving remote UI inside the
                        internal network.
  --ap-wlan AP_WLAN     network interface that will be used to create hotspot.
                        'wlp4s0' is default.
  --ap-inet AP_INET     forwarding interface. Default is None.
  --ap-ip AP_IP         ip address of this machine in new network.
                        192.168.45.1 is default.
  --ap-netmask AP_NETMASK
                        access point netmask address. 255.255.255.0 is
                        default.
  --ssid SSID           Preferred access point name. 'T_System' is default.
  --password PASSWORD   Password of the access point. 't_system' is default.
  --inet INET           forwarding interface. Default is None.
  --static-ip STATIC_IP
                        static ip address in connected external network.
                        192.168.45.1 is default.
  --netmask NETMASK     netmask address. 255.255.255.0 is default.

external network options:
  --wlan WLAN           network interface that will be used to connect to
                        external network. 'wlp4s0' is default.

others:
  -S, --show-stream     Display the camera stream. Enable the stream
                        window.(Require gui environment.)
  -m FOUND_OBJECT_MARK, --found-object-mark FOUND_OBJECT_MARK
                        Specify the mark type of the found object. To use:
                        either `single_rect`, `rotating_arcs`, `partial_rect`
                        or None. Default is `single_rect`
  -r, --record          Record the video stream. Files are named by the date.
  --version             Display the version number of T_System.
```

<br>

### Interfaces

#### Official Stand

Portable usage interface v0.3.1

<img align="left" width="420" height="430" src="https://raw.githubusercontent.com/Connected-life/T_System/master/docs/img/official_stand/v0.3.1/back_render.jpg">
<img align="center" width="420" height="430" src="https://raw.githubusercontent.com/Connected-life/T_System/master/docs/img/official_stand/v0.3.1/front_render.jpg">

<br>

- Dependencies
    -
    - Raspberry pi 3 model B/B+ or Asus Tinker board.
    - 5 piece sg90 or mg90s servo motors.   
                   
- Properties
    -   
    - 1 switch key for on/off
        -
            Cut the electiric current directly
    - 4 pieces 18650 li-ion batteries
        -
            Parallel connected sources.
    - Internal cooler
        -
            A micro fan for falling down the cpu temperature.
    - Local network Management
        -
            Scan the around networks. If there is no network connection become an Access Point and serve Remote UI ınteernally.
    - Remote UI accessing
        -
            No control by tapping. Accessing with Remote UI from mobile or desktop.

<sup><i>To see the old version explainings go [here](https://raw.githubusercontent.com/Connected-life/T_System/master/docs/stand/README.me)</i></sup>

#### Remote UI

The remotely controlling interface v0.2.72

- Properties
    -             
    - Motion control
        -
            2 kind control type for the arm. 
                
                1: axis based control. move all axes separately.
                2: direction based control. move according the direction (up-down/forward-backward/right-left).
    - Scenario Control
        -
            create scenarios by specifying arm positions and generating motion paths with them for behaving like a camera dolly.
    - Previewing
        -
            watch the live video stream during creating scenarios and monitor what is it recording on working.

<sup><i>Powered by "flask" as an embedded framework. Available on mobile or desktop.</i></sup> 

#### Augmented

Augmented usage explained [here](https://github.com/MCYBA/A.V.A.) into the `AUGMENTED.md`.

<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

### Contribute

If you want to contribute to Dragonfire then please read [this guide](https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md#contributing-to-dragonfire).

Please consider to support us with buying a coffee:
<a href="https://www.buymeacoffee.com/tsystem" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
