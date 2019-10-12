# T_System

the (non-)moving objects tracking system via two axis camera motion and n joint robotic arm for raspberry pi distributions

<p align="center" >
<a href="https://github.com/connected-life/T_System/graphs/contributors"><img src="https://img.shields.io/github/contributors/connected-life/T_System" alt="Github contributors"/></a>
<a href="https://github.com/connected-life/T_System"><img src="https://img.shields.io/github/release-pre/connected-life/T_System" alt="Github release"/></a>
<a href="https://github.com/connected-life/T_System/stargazers"><img src="https://img.shields.io/github/stars/connected-life/T_System" alt="Github stars"/></a>
</p>

[![Badge Emoji](https://img.shields.io/badge/emoji-%F0%9F%A6%84%20%F0%9F%92%9F-lightgrey.svg)](https://en.wikipedia.org/wiki/Emoji#Unicode_blocks)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[![Travis](https://api.travis-ci.org/connected-life/T_System.svg?branch=master)](https://travis-ci.org/connected-life/T_System)
[![Read The Docs](https://readthedocs.org/projects/t-system/badge/?version=latest)](https://t-system.readthedocs.io/en/latest/?badge=latest)
[![Coveralls](https://coveralls.io/repos/github/connected-life/T_System/badge.svg)](https://coveralls.io/github/connected-life/T_System/)
[![Pyup shield](https://pyup.io/repos/github/connected-life/T_System/shield.svg?label=pyup&color=brightgreen)](https://pyup.io/repos/github/connected-life/T_System/)
[![Pyup python-3 shield](https://pyup.io/repos/github/connected-life/T_System/python-3-shield.svg?label=python%203&color=brightgreen)](https://pyup.io/repos/github/connected-life/T_System/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](code-of-conduct.md)


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

- All requirement libraries automatically installing via installation scripts. To see these libraries look at [here](https://github.com/connected-life/T_System/blob/master/docs/requirements.txt)

### Installation

Clone the GitHub repository and run

```Shell
sudo ./install.sh
```

in the repository directory.

for development mode: `sudo ./install-dev.sh`

<sup><i>If there is a failure try `sudo -H ./install-dev.sh`</i></sup>

### Usage <a href="https://t-system.readthedocs.io/en/latest/t_system.html"><img src="https://media.readthedocs.com/corporate/img/header-logo.png" align="right" height="25px" /></a>

```Shell
usage: t_system [-h] [--interface {official_stand,augmented,remote_ui,None}]
                [--stand-gpios RED-LED GREEN-LED FAN] [--host HOST]
                [--port PORT] [--debug] [-l] [-s]
                [--detection-model DETECTION_MODEL]
                [--cascade-file CASCADE_FILE] [-j]
                [--encoding-file ENCODING_FILE] [--use-tracking-api]
                [--tracker-type {BOOSTING,MIL,KCF,TLD,MEDIANFLOW,GOTURN,MOSSE,CSRT}]
                [--resolution WIDTH HEIGHT] [--framerate FRAMERATE]
                [--chunk CHUNK] [--rate RATE] [--channels CHANNELS]
                [--audio_device_index AUDIO_DEVICE_INDEX]
                [--record-formats VIDEO AUDIO MERGED] [--robotic-arm ARM]
                [--ls-gpios PAN TILT]
                [--AI AI | --non-moving-target | --arm-expansion] [-p]
                [--ap-wlan AP_WLAN] [--ap-inet AP_INET] [--ap-ip AP_IP]
                [--ap-netmask AP_NETMASK] [--ssid SSID] [--password PASSWORD]
                [--wlan WLAN] [--inet INET] [--static-ip STATIC_IP]
                [--netmask NETMASK] [--country-code COUNTRY_CODE]
                [--environment {production,development,testing}]
                [--no-emotion] [-S]
                [-m {single_rect,rotating_arcs,partial_rect,animation_1,None}]
                [-r] [-v] [--version]
                {id,remote-ui-authentication,face-encoding,self-update} ...

positional arguments:
  {id,remote-ui-authentication,face-encoding,self-update}
                        officiate the sub-jobs
    id                  Make identification jobs of T_System.
    remote-ui-authentication
                        Remote UI administrator authority settings of the
                        secret entry point that is the new network connection
                        panel.
    face-encoding       Generate encoded data from the dataset folder to
                        recognize the man T_System is monitoring during
                        operation.
    self-update         Update source code of t_system itself via `git pull`
                        command from the remote git repo.

optional arguments:
  -h, --help            show this help message and exit
```
<sup>For detailed output look at [Help](https://github.com/connected-life/T_System/blob/master/USAGE.md#help-output)</sup>

`t_system user-interfaces {official_stand,augmented,remote_ui,None}` is standard running command.

`official_stand`, `augmented` and `remote_ui` are mentioned [here](#official-stand), [here](#augmented) and [here](#remote-ui) as respectively. 

<sup>Detailed usage available inside [`USAGE.md`](https://github.com/connected-life/T_System/blob/master/USAGE.md)</sup>

### Interfaces

#### Official Stand

Portable usage interface v0.5

<img align="left" width="400" height="430" src="https://raw.githubusercontent.com/Connected-life/T_System/master/docs/img/official_stand/v0.5/back_render.jpg">
<img align="center" width="320" height="430" src="https://raw.githubusercontent.com/Connected-life/T_System/master/docs/img/official_stand/v0.5/front_render.jpg">

<br>

- Dependencies
    -
    - Raspberry pi 4 model B/B+.
    - 2 pieces mg995, 3 pieces sg90 or mg90s servo motors.   
                   
- Properties
    -
    1.25 times bigger than the previous version.
    
    - Tiny Camera
        -
            8x8mm dimensions 8MP resolution micro camera.
    - IR led
        -
            Automatically activatable IR led for advanced night vision. 
    - 1 switch key for on/off
        -
            Cut the electiric current directly.
    - 4 pieces 18650 li-ion batteries
        -
            Parallel connected sources.
    - Internal Cooler
        -
            2 pieces 30x30x10mm micro fan and the aluminyum block for falling down the cpu temperature.
    - Local Network Management
        -
            Scan the around networks. If there is no network connection become an Access Point and serve Remote UI ınternally.
    - Remote UI accessing
        -
            No control by tapping. Accessing with Remote UI from mobile or desktop.

<sup><i>To see the old version explaining go [here](https://github.com/Connected-life/T_System/blob/master/docs/stand/README.md)</i></sup>

#### Remote UI

The remotely controlling interface v0.9.69

- Properties
    -             
    - Motion Control
        -
            2 kind control type for the arm. 
                
                1: axis based control. move all axes separately.
                2: direction based control. move according the direction (up-down/forward-backward/right-left).
    - Scenario Control
        -
            create scenarios by specifying arm positions and generating motion paths with them for behaving like a camera dolly.
    - Previewing / Monitoring
        -
            watch the live video stream during creating scenarios and monitor what is it recording on working.
    - Network Control
        -
            Add, update or delete Wi-Fi connection info.
    - Recognize People
        -
            Add, update and delete the photos of the people for recognizing them. Choose one, more or all and recognize during the job.
    - Record Control
        -
            Get preview or download the video records with the date based sorting system.

<sup><i>Powered by "flask" as an embedded framework. Available on mobile and desktop.</i></sup> 

#### Augmented

Augmented usage explained [here](https://github.com/MCYBA/A.V.A.) into the `AUGMENTED.md`.

<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

### Contribute

If you want to contribute to T_System then please read [this guide](https://github.com/connected-life/T_System/blob/master/CONTRIBUTING.md#contributing-to-t_system).

Please consider to support us with buying a coffee:
<a href="https://www.buymeacoffee.com/tsystem" target="_blank"><img src="https://bmc-cdn.nyc3.digitaloceanspaces.com/BMC-button-images/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>
