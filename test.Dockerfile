# Use an official Python runtime as a parent image
FROM raspbian/stretch
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV PYTHONUNBUFFERED 1

# Maintainer
MAINTAINER Cem Baybars GÜÇLÜ "cem.baybars@gmail.com"

# Install all APT dependencies
RUN apt-get update
RUN apt-get -qqy install python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev
RUN apt-get -qqy install python3-minimal ${misc:Pre-Depends}
RUN apt-get -qqy install ${python3:Depends} ${misc:Depends} flite portaudio19-dev python3-all-dev flac libnotify-bin python-egenix-mx-base-dev python3-lxml python3-pyaudio python3-httplib2 python3-pip python-flake8 libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool
RUN apt-get -qqy install dnsmasq hostapd

## Install OpenCV
RUN apt-get -qqy install build-essential
RUN apt-get -qqy install cmake git unzip libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
RUN apt-get install -qqy python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/Itseez/opencv/archive/3.2.0.zip && \
    unzip 3.2.0.zip && rm 3.2.0.zip && \
    cd opencv-3.2.0 && mkdir build && \
    cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D BUILD_EXAMPLES=ON .. && \
    make -j6 && make install && \
    ldconfig

# Install dependency dlib
RUN cd ~ && mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install pip3
RUN apt-get install -y python3-pip

# Install T_System Python package
RUN pip3 install .

# Define environment variables
ENV T_SYSTEM_DIR /usr/share/t_system

# Create the necessary directories for the Tensorflow models
RUN mkdir $T_SYSTEM_DIR

# Retry to install the Python package dependencies in case of a failure
RUN pip3 install --upgrade picamera>=1.13 RPi.GPIO>=0.6.5 tinydb==3.9.0.post1 numpy paho-mqtt>=1.4.0 face_recognition multipledispatch wireless netifaces psutil pyaccesspoint wifi flask schema gitpython elevate imutils gpiozero
RUN pip3 install pytest-faulthandler
RUN pip3 install --upgrade flake8 sphinx sphinx_rtd_theme recommonmark m2r pytest docutils

# Print success message
RUN echo -e "\n\T_System is successfully installed into the container.\n"

# Make port 3301 available to the world outside this container
EXPOSE 3301

# Start test
ENTRYPOINT ["/usr/local/bin/python3", "pytest"]

# Default arguments
CMD ["--capture=sys"]
