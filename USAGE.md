# Usage

T_System has 4 different ways to control. Strong to weak, respectively:

- Command-line tools
- Remote UI
- Augmented
- Official Stand

First of all excluding command-line tools, all control ways are the user interfaces at the same time and they can be activate with using each other.

### Command-line Tools

Selecting the all user interfaces can make with positional `interface` argument. With `-h` or `--help` flag, all abilities of T_System can be shown. 
But there is few important feature those need the  detailed explanation:

#### Sub-commands

- `remote-ui-authentication`
    - There is a secret administration entry in T_System Remote UI.
    When the user write the correct pattern inside to Wi-Fi ssid and
    password fields, administration authenticate will activated. Initial 
    setting of T_System there is a creator authentication keys. So if 
    you want to be admin for Remote UI, you have to change this secret
    ssid and passwords patterns. With this command:
    
      `t_system remote-ui-authentication --ssid <SSID> --password <PASSWORD>`
    
      You can be create your own secret administration entry.
      
    - `encode-face`
    
    - `self-update`


### Remote UI
### Augmented
### Official Stand

### Help Output

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
                {id,remote-ui-authentication,encode-face,self-update} ...

positional arguments:
  {id,remote-ui-authentication,encode-face,self-update}
                        officiate the sub-jobs
    id                  Make identification jobs of T_System.
    remote-ui-authentication
                        Remote UI administrator authority settings of the
                        secret entry point that is the new network connection
                        panel.
    encode-face       Generate encoded data from the dataset folder to
                        recognize the man T_System is monitoring during
                        operation.
    self-update         Update source code of t_system itself via `git pull`
                        command from the remote git repo.

optional arguments:
  -h, --help            show this help message and exit

user-interfaces:
  --interface {official_stand,augmented,remote_ui,None}
                        Set the user interfaces. To use: either
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
  --stand-gpios RED-LED GREEN-LED FAN
                        GPIO pin numbers of official stand's LEDs and fans.
                        5(as red led), 6(as green led) and 14(as fan) GPIO
                        pins are default.

remote_ui:
  --host HOST           Specify host address.
  --port PORT           Specify the port.
  --debug               Activate debug mode.

Running Modes:
  -l, --learn           Teach Mode. Teach the object tracking parameters with
                        the trial and error method.
  -s, --security        Security Mode. Scan the around and optionally take
                        photos of visitors.

Running Tools:
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
                        for recognize object. Sample: 'jane_encoding' for
                        jane_encoding.pickle file under the
                        '.t_system/recognition/encodings' folder in your Home
                        directory. If `main_encoding` chosen,
                        `main_encoding.pickle` file that creates from merging
                        all encoding files under `.../encodings` folder will
                        used. Default is `main_encoding`
  --use-tracking-api    Use the openCV's tracking API for realize the next
                        object is same as previous one.
  --tracker-type {BOOSTING,MIL,KCF,TLD,MEDIANFLOW,GOTURN,MOSSE,CSRT}
                        OpenCV's tracking type to use: either `BOOSTING`,
                        `MIL`, `KCF`, `TLD`, `MEDIANFLOW`, `GOTURN`, `MOSSE`
                        or `CSRT`. `CSRT` is default.

Video Options:
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
  --record-formats VIDEO AUDIO MERGED
                        Formats for recording the work. `h264` and `wav` for
                        separate video and audio recording and `mp4` for
                        merged file are default.

Motion Mechanism:
  --robotic-arm ARM     One of the robotic arm names those are defined in
                        config.json file of arm module. The arm is for relocating the 2
                        axis target locking system hybrid-synchronously.

Target Locking System:
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
  --arm-expansion       Use the Target Locking System as the extension of the
                        Robotic Arm. Don't use AI or OpenCv's object detection
                        methods. Add 2 more joints to the Robotic Arm

Access Point Options:
  -p, --access-point    Become access point for serving remote UI inside the
                        internal network.
  --ap-wlan AP_WLAN     Network interface that will be used to create HotSpot.
                        'wlan0' is default.
  --ap-inet AP_INET     Forwarding interface. Default is None.
  --ap-ip AP_IP         Ip address of this machine in new network.
                        192.168.45.1 is default.
  --ap-netmask AP_NETMASK
                        Access Point netmask address. 255.255.255.0 is
                        default.
  --ssid SSID           Preferred access point name. 'T_System' is default.
  --password PASSWORD   Password of the access point. 't_system' is default.

External Network Options:
  --wlan WLAN           network interface that will be used to connect to
                        external network. 'wlan0' is default.
  --inet INET           Forwarding interface. Default is None.
  --static-ip STATIC_IP
                        The static IP address for the connected external
                        network, if wanted.
  --netmask NETMASK     Netmask address. 255.255.255.0 is default.
  --country-code COUNTRY_CODE
                        Wifi country code for the wpa_supplicant.conf. To use
                        look at: https://github.com/recalbox/recalbox-
                        os/wiki/Wifi-country-code-(EN). Default is `TR`

Others:
  --environment {production,development,testing}
                        The running environment. It specify the configuration
                        files and logs. To use: either `production`,
                        `development` or `testing`. Default is production
  --no-emotion          Do not mak feelings with using motion mechanisms.(Arm
                        and Locking System.)
  -S, --show-stream     Display the camera stream. Enable the stream
                        window.(Require gui environment.)
  -m {single_rect,rotating_arcs,partial_rect,animation_1,None}, --found-object-mark {single_rect,rotating_arcs,partial_rect,animation_1,None}
                        Specify the mark type of the found object. To use:
                        either `single_rect`, `rotating_arcs`, `partial_rect`
                        or None. Default is `single_rect`
  -r, --record          Record the video stream. Files are named by the date.
  -v, --verbose         Print various debugging logs to console for debug
                        problems
  --version             Display the version number of T_System.
```

