# Usage

T_System has 4 different ways to control. Strong to weak, respectively:

- Command-line tools
- Remote UI
- Augmented
- Official Stand

First of all excluding command-line tools, all control ways are the user
interfaces at the same time and they can be activate with using each other.

### Command-line Tools

Selecting the all user interfaces can make with positional `interface` argument.
With `-h` or `--help` flag, all abilities of T_System can be shown. 
But there is few important feature those need the  detailed explanation:

#### Sub-commands

- `id`
    - Each device that powered by T_System has unique IDs.
    T_System has private and public IDs and user specified Name.
    These public/private IDs pair and Name been uses for reaching to 
    T_System from remote UI.
      
      Only Name can be changed by remote UI public and private IDs can be
    changes via command-line. For more details about usage of `id` 
    sub-command:
        
        `t_system id --help`
    
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
    - T_System has face recognition ability via `face_recognition` python
    module. For recognizing faces, it have to has encoded face data. Via 
    Remote UI, photos that have faces, can be uploaded to T_System and it
    creates encoded data automatically. And also for this process command-line
    is available: For more details about usage:
    
        `t_system encode-face --help`
    
- `self-update`
    - For Firmware(include Remote UI) update, T_System has `self-update`
    sub-command. Currently, when any update published via GitHub, T_System
    can check this information and update itself. Via Remote UI, automatic
    update task can be handled so if user don't want to realize automatic
    update, he/she can disable this feature. and the via the `self-update`
    sub-command, updation check and realize can be executed:
        
        `t_system self-update --help`

- `arm`
    - For the robotic arm of the T_System that uses for Executing of scenarios
    and making emotions, there is customization field. The developers and
    the professional users, can be create their own robotic arm and
    configuration information of this arm in `t_system/motion/arm.config.json`
    file.
    
      Via this configuration information, T_System creates a model of 
    the arm and this model been uses for forward and inverse kinematics solving.
    There is example configuration info in file that aforementioned above.
    For sub-command usage details:
    
        `t_system arm --help`

- `live-stream`
    - T_System has Live Video Streaming ability powered by FFmpeg.
    Currently, Live-Streaming can be realize on 8 stream permissive websites
    (include YouTube, facebook, periscope, and twitch). Live-Streaming activation
    and deactivation process can be handled by Remote UI.
    
      And adding new websites, adding new accounts for this websites can be
    realize by Remote UI and command-line. For the Remote UI only the person who
    has administration authentication can create new Websites. For more usage
    detail of `live-stream` sub-command:
    
        `t_system live-stream --help`

- `r-sync`
    - For reaching recorded videos of photos from your cloud storage account
    when and where-ever you want, T_System has Remote Storage Synchronization
    ability. For now, it is available with Dropbox. 
    
      Remote Sync activation and deactivation process, adding new accounts
    for available services can be realize by Remote UI and command-line.
    For more usage detail of `r-sync` sub-command:
    
        `t_system live-stream --help`

- `log`
    - Viewing and deleting the logs of T_System are available with command-line
    and Remote UI. Realizing this jobs by Remote UI, administration privileges
    required. For more usage detail of `log` sub-command:
        
        `t_system log --help`

### Remote UI

T_System has `flask` powered Javascript codded controlling Interface that called as `remote_ui`.
Any person who has network connection with T_System can be create a request to `5000` port
of the T_System IP, and the front-end of the UI will return to him/her. For connecting to the
T_System safely, [there](https://github.com/LookAtMe-Genius-Cameraman/LookAtMe-app) is an mobile app
and available on Google's Play Store. If the user has T_System's unique public ID or determined a Name
by him/her-self, He/She can be connected to T_System and start controlling it.

There is and advanced field, for professional users and it can be activated via `advanced` option of
Remote UI's options window.

Also for the administration authentication of Remote UI, please read `remote-ui-authentication`
section under [there](#sub-commands).
 
### Augmented
### Official Stand

### Help Output

```Shell
usage: t_system [-h] [--interface {official_stand,augmented,remote_ui,None}]
                [--stand-gpios RED-LED GREEN-LED FAN] [--host HOST]
                [--port PORT] [--debug] [-l] [-s]
                [--detection-model DETECTION_MODEL] [--cascades CASCADES] [-j]
                [--encoding-file ENCODING_FILE] [--use-tracking-api]
                [--tracker-type {BOOSTING,MIL,KCF,TLD,MEDIANFLOW,GOTURN,MOSSE,CSRT}]
                [--camera-rotation CAMERA_ROTATION]
                [--resolution WIDTH HEIGHT] [--framerate FRAMERATE]
                [--chunk CHUNK] [--rate RATE] [--channels CHANNELS]
                [--audio_device_index AUDIO_DEVICE_INDEX]
                [--shoot-formats VIDEO AUDIO MERGED] [--shot-format SHOT] [-x]
                [--sd-channels SD_CHANNELS] [--arm-name ARM]
                [--ls-gpios PAN TILT] [--ls-channels PAN TILT]
                [--AI AI | --non-moving-target | --arm-expansion] [-p]
                [--ap-wlan AP_WLAN] [--ap-inet AP_INET] [--ap-ip AP_IP]
                [--ap-netmask AP_NETMASK] [--ssid SSID] [--password PASSWORD]
                [--wlan WLAN] [--inet INET] [--static-ip STATIC_IP]
                [--netmask NETMASK] [--country-code COUNTRY_CODE]
                [--environment {production,development,testing}]
                [--no-emotion] [-S]
                [-m {single_rect,rotating_arcs,partial_rect,animation_1,None}]
                [-r] [-v] [--version]
                {id,remote-ui-authentication,encode-face,self-update,arm,live-stream,r-sync,log}
                ...

positional arguments:
  {id,remote-ui-authentication,encode-face,self-update,arm,live-stream,r-sync,log}
                        officiate the sub-jobs
    id                  Make identification jobs of T_System.
    remote-ui-authentication
                        Remote UI administrator authority settings of the
                        secret entry point that is the new network connection
                        panel.
    encode-face         Generate encoded data from the dataset folder to
                        recognize the man T_System is monitoring during
                        operation.
    self-update         Update source code of t_system itself via `git pull`
                        command from the remote git repo.
    arm                 Management jobs of Denavit-Hartenberg transform matrix
                        models of robotic arms of T_System.
    live-stream         Make Online Stream jobs of T_System.
    r-sync              Make remote synchronization jobs of T_System.
    log                 Make logging jobs of T_System.

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
  --cascades CASCADES   Specify the trained detection algorithm file for the
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

Camera Options:
  --camera-rotation CAMERA_ROTATION
                        Specify the camera's ratational position. 180 degree
                        is default.
  --resolution WIDTH HEIGHT
                        Specify the camera's resolution of vision ability.
                        320x240 is default

Shoot Options:
  --framerate FRAMERATE
                        Specify the camera's framerate. of vision ability. 32
                        fps is default.
  --chunk CHUNK         Smallest unit of audio. 1024*8=8192 bytes are default.
  --rate RATE           Bit Rate of audio stream / Frame Rate. 44100 Hz sample
                        rate is default.
  --channels CHANNELS   Number of microphone's channels. Default value is 1.
  --audio_device_index AUDIO_DEVICE_INDEX
                        Index of the using audio device. 2 is default.
  --shoot-formats VIDEO AUDIO MERGED
                        Formats for recording the work. `h264` and `wav` for
                        separate video and audio recording and `mp4` for
                        merged file are default.

Shot Options:
  --shot-format SHOT    Format for take shots. `jpg` is default

Motion Mechanism:
  -x, --ext-servo-driver
                        Use external servo motor driver board.
  --sd-channels SD_CHANNELS
                        Number of external servo driver's channels. Default
                        value is 16.

Robotic Arm:
  --arm-name ARM        One of the robotic arm names those are defined in
                        config.json file. The arm is for relocating the 2 axis
                        target locking system hybrid-synchronously.

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
