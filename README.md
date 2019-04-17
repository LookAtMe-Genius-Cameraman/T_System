# T_System


the moving objects tracking system via two axis camera motion for raspberry pi distributions

![A.V.A.](https://raw.githubusercontent.com/MCYBA/T_System/master/docs/img/on_work.gif)

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
- 2 servo motors
- 2 axis motion system as pan-tilt motions

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
usage: t_system [-h] [-S] [-l] [-s] [-a] [-d DETECTION_MODEL] [-j] [--version]
                [--gpio-pan-tilt PAN TILT] [--encoding-file ENCODING_FILE]
                [--cascade-file CASCADE_FILE] [--use-tracking-api]
                [--tracker-type TRACKER_TYPE]

optional arguments:
  -h, --help            show this help message and exit
  -S, --show-stream     Display the camera stream. Enable the stream
                        window.(Require gui environment.)
  -l, --learn           Teach Mode. Teach the object tracking parameters with
                        the trial and error method.
  -s, --security        Security Mode. Scan the around and optionally take
                        photos of visitors.
  -a, --augmented       Augmented control with the Augmented Virtual Assistant
                        A.V.A.. 'https://github.com/MCYBA/A.V.A.' is the home
                        page of the A.V.A. and usage explained into the
                        'AUGMENTED.md'.
  -d DETECTION_MODEL, --detection-model DETECTION_MODEL
                        Object detection model to use: either `haarcascade`,
                        `hog` or `cnn`. `hog` and `cnn` can only use for
                        detecting faces. `haarcascade` is default.
  -j, --no-recognize    Do not recognize the things.(faces, objects etc.)
  --version             Display the version number of T_System.
  --gpio-pan-tilt PAN TILT
                        GPIO pin numbers of the 2 axis moving platform's servo
                        motors. 17(as pan) and 14(as tilt) GPIO pins are
                        default.
  --encoding-file ENCODING_FILE
                        Specify the trained recognition encoding pickle file
                        for recognize object. Sample: 'encodings' for
                        encodings.pickle file under the
                        'recognition_encodings' folder.
  --cascade-file CASCADE_FILE
                        Specify the trained detection algorithm file for the
                        object detection ability. Sample:
                        'frontalface_default' for frontalface_default.xml file
                        under the 'haarcascade' folder.
  --use-tracking-api    Use the openCV's tracking API for realize the next
                        object is same as previous one.
  --tracker-type TRACKER_TYPE
                        OpenCV's tracking type to use: either `BOOSTING`,
                        `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE`
                        or `CSRT`. `CSRT is default.`
```

<br>

### Augmented

Augmented usage explained [here](https://github.com/MCYBA/A.V.A.) into the `AUGMENTED.md`.

<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

