# Use an official Python runtime as a parent image
FROM resin/rpi-raspbian
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV PYTHONUNBUFFERED 1

# Maintainer
MAINTAINER Cem Baybars GÜÇLÜ "cem.byabars@gmail.com"

# Install all APT dependencies
RUN apt-get update
RUN apt-get -qqy install python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev
RUN apt-get -qqy install python3-minimal ${misc:Pre-Depends}
RUN apt-get -qqy install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python-egenix-mx-base-dev python3-lxml python3-pyaudio python3-httplib2 python3-pip libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool
RUN apt-get -qqy install dnsmasq hostapd

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install pip3
RUN apt-get install -y python3-pip

# Install Dragonfire Python package
RUN pip3 install .

# Define environment variables
ENV T_SYSTEM_DIR /usr/share/t_system

# Create the necessary directories for the Tensorflow models
RUN mkdir $T_SYSTEM_DIR

# Retry to install the Python package dependencies in case of a failure
RUN pip3 install --upgrade picamera>=1.13 RPi.GPIO>=0.6.5 tinydb==3.9.0.post1 numpy paho-mqtt>=1.4.0 face_recognition multipledispatch wireless netifaces psutil pyaccesspoint wifi flask schema gitpython elevate imutils gpiozero

# Print success message
RUN echo -e "\n\T_System is successfully installed into the container.\n"

# Make port 3301 available to the world outside this container
EXPOSE 3301

# Start T_System
ENTRYPOINT ["t_system"]

# Default arguments
CMD ["None", "-S", "-j"]
