#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: online_stream
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's online stream broadcast feature of augmented ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import io
import time  # Time access and conversions

from picamera import PiCamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE = """<html>
            <head>
                <title>Eye of Object Tracking System</title>
            </head>
            <body>
                <center>
                    <h1>Eye of Object Tracking System
                    </h1>
                </center>
                <center>
                    <img src="stream.mjpg" width="800" height="600">
                </center>
            </body>
          </html>
       """


class StreamingOutput(object):
    """Class to provide output of the live stream of augmented mode.
    """
    def __init__(self):
        """Initialization method of :class:`t_system.augmented.StreamingOutput` class.
        """
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        """Function to provide writing buffer via buf parameter.

        Args:
                buf:         buffer parameter.
        Returns:
                object:
        """
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    """Class to provide the streaming handler.
    """

    def do_GET(self):
        """Function to provide setting stream.
        """
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    """Class to provide the server of streaming.
    """
    allow_reuse_address = True
    daemon_threads = True


def start_stream(stop_thread, camera):
    """Function to start the online and live video stream.

    Args:
            stop_thread:       	    Stop flag of the tread about terminating it outside of the function's loop.
            camera:       	        Camera object from PiCamera.
    """
    output = StreamingOutput()
    # Uncomment the next line to change your Pi's Camera rotation (in degrees)
    # camera.rotation = 90
    camera.start_recording(output, video_format='mjpeg')
    try:
        address = ('10.42.0.151', 8000)
        server = StreamingServer(address, StreamingHandler)
        is_server_active = False
        while True:
            if not is_server_active:
                server.serve_forever()
                is_server_active = True
            if stop_thread():
                server.server_close()
                break
            time.sleep(0.5)
    finally:
        camera.stop_recording()


if __name__ == '__main__':

    # FOLLOWING LINES FOR THE TESTING THE "online_stream" SUBMODULE!!
    with PiCamera(resolution='800x600', framerate=24) as camera:
        output = StreamingOutput()
        # Uncomment the next line to change your Pi's Camera rotation (in degrees)
        # camera.rotation = 90
        camera.start_recording(output, video_format='mjpeg')
        try:
            address = ('10.42.0.151', 8000)
            server = StreamingServer(address, StreamingHandler)
            server.serve_forever()
        finally:
            camera.stop_recording()
