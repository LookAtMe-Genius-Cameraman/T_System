# T_System


the moving objects tracking system via two axis camera motion for raspberry pi distributions

<br>


#### Supported Environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | Raspbian         |
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

- OpenCV. Install via [here](https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html) or any other place you want.

### Installation

Download the [latest release](https://github.com/DragonComputer/Dragonfire/releases/latest) (the `.deb` file) and:

```Shell
sudo ./install.sh
```
for development mode: `sudo ./install-dev.sh`


<sup><i>If there is a failure try `sudo -H ./install-dev.sh`</i></sup>

### Usage

```
usage: t_system [-h] [-c] [-s] [-j] [-v] [-g]
                  [--version]

optional arguments:
  arguments not defined yet.
```


<br>


<br>

**Supported Distributions:** Raspbian. This release is fully supported. Any other Debian based ARM architecture distributions are partially supported.

