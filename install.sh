#!/bin/bash
OPTS=`getopt -o n --long no-model -- "$@"`
if [[ $? != 0 ]] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi
eval set -- "${OPTS}"

apt-get update
apt-get -y install debhelper python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev pkg-config cmake && \
apt-get -y install dpkg python3-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python3-lxml python3-pyaudio python3-httplib2 python3-pip python3-setuptools python3-wheel python-opencv libavcodec-dev libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool libgtk2.0-0 gir1.2-gtk-3.0 dbus libdbus-glib-1-dev libdbus-1-dev python-dbus && \
apt-get -y install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev libtiff5-dev libpng12-dev libavformat-dev libswscale-dev libv4l-dev libgtk-3-dev libavformat-dev openexr libopenexr-dev libqt4-dev libgstreamer0.10-0-dbg libgstreamer0.10-0 libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
apt-get -y install dnsmasq hostapd
apt-get -y install figlet boxes lolcat

pip3 install .

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

T_SYSTEM_DIR=/usr/share/t_system
if [[ ! -d "$T_SYSTEM_DIR" ]]; then
  mkdir ${T_SYSTEM_DIR}
fi

pip3 install --upgrade picamera>=1.13 RPi.GPIO>=0.6.5 tinydb==3.9.0.post1 numpy paho-mqtt>=1.4.0 face_recognition dlib multipledispatch wireless netifaces psutil pyaccesspoint wifi flask schema gitpython elevate imutils gpiozero requests pyroute2 pexpect opencv-python opencv-contrib-python board adafruit-blinka adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit && \
pip3 install --upgrade flake8 sphinx sphinx_rtd_theme recommonmark m2r pytest docutils && \
echo -e "\n\n${GREEN}t_system is successfully installed to your computer.${NC}\n"
