#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: high_tech_aim
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to high tech targeting mark of T_System's vision ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""
import numpy
import cv2

from math import sqrt, radians, cos, sin


class Aimer():
    """Class to draw a high tech aim mark.

    This class provides necessary initiations and a function named :func:`t_system.high_tech_aim.Aimer.mark`
    for draw the targeting mark.
    """

    def __init__(self):
        """Initialization method of :class:`t_system.high_tech_aim.Aimer` class.
        """

        self.image = None
        self.image_width = 0
        self.image_height = 0

        self.object_distance = ""
        self.text_font = cv2.FONT_HERSHEY_SIMPLEX

        self.arc_direction = True

        self.thin_arc_start_angle = 170
        self.thin_arc_end_angle = 310
        self.thick_arc_start_angle = 180
        self.thick_arc_end_angle = 300

    def mark(self, image, center, radius, physically_distance, color='red'):
        """The top-level method to draw target mark like high tech.

        Args:
                image:       	        Image matrix.
                center:       	        Center point of the aimed object.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color:                  The dominant color of the targeting mark.
        """
        self.image = image
        self.object_distance = str(round(physically_distance * 0.164 / 1000, 2)) + " m"  # 0.164 mm is the length of one pixel.

        radius *= 0.515
        thickness = radius * 0.23
        self.image_height, self.image_width = self.image.shape[:2]

        center_x = center[0]
        center_y = center[1]

        self.draw_arc(center_x, center_y, radius, thickness, self.thick_arc_start_angle, self.thick_arc_end_angle)
        self.draw_arc(center_x, center_y, radius * 0.95, thickness * 0.15, self.thin_arc_start_angle, self.thin_arc_end_angle)

        text_point = (int(center_x - radius * 0.1), int(center_y + radius * 0.95 - radius * 0.1))
        cv2.putText(self.image, self.object_distance, text_point, self.text_font, radius * 0.004, (0, 0, 200), int(radius * 0.004), cv2.LINE_AA)
        # parameters: image, put text, text's coordinates,font, scale, color, thickness, line type(this type is best for texts.)

        self.check_angle_of_arcs()

        self.rotate_arcs()

        return self.image

    def draw_arc(self, center_x, center_y, radius, thickness, start_angle, end_angle, edge_shine=False):
        """The low-level method to draw arcs of the mark.

        Args:
                center_x:       	  The object's x center(by column count).
                center_y:             The object's y center(by row count).
                radius:               Radius of the aim.
                thickness:            Thickness of arc.
                start_angle:          Start angle of the arc.
                end_angle:            End angle of the arc.
                edge_shine:           Flag for the activate te shining of the arc's edge.
        """

        if end_angle >= start_angle:
            pass
        else:
            start_angle, end_angle = end_angle, start_angle

        rad = radius
        while rad <= radius + thickness:
            angle = start_angle
            while angle <= end_angle:
                x = center_x + rad * cos(radians(angle))
                y = center_y - rad * sin(radians(angle))
                if self.image_width >= x >= 0 and self.image_height >= y >= 0:  # for the frames' limit protection.
                    distance = int(sqrt((center_x - x) * (center_x - x) + (center_y - y) * (center_y - y)))
                    x = int(x)
                    y = int(y)
                    if radius <= distance <= radius + thickness:
                        [b, g, r] = self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, 0, 1])

                        # Following lines are for increase the visibility when the "mark" comes on the dark areas.
                        if r <= 100:
                            if r == 0:
                                r = 1
                                self.image[y, x] = [0, 0, 1]
                            redness_rate = (255 / r) / 0.12
                            self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, 0, redness_rate])

                        if edge_shine:
                            for thick in range(60, 100, 4):
                                if radius + thickness * thick / 100 <= distance <= radius + thickness:
                                    # [b, g, r] = self.image[y, x]
                                    self.image[y, x] = numpy.array(self.image[y, x]) + numpy.array([r * 0.08, r * 0.08, 255])
                angle += 0.25
            rad += 1

    def check_angle_of_arcs(self):
        """The low-level method to limit the value of the arc's angle.
        """

        if self.thin_arc_start_angle >= 3600:
            self.thin_arc_start_angle %= 360
            self.thin_arc_start_angle += 360

        elif self.thin_arc_start_angle <= -3600:
            self.thin_arc_start_angle %= 360
            self.thin_arc_start_angle -= 360

        if self.thin_arc_end_angle >= 3600:
            self.thin_arc_end_angle %= 360
            self.thin_arc_end_angle += 360

        elif self.thin_arc_end_angle <= -3600:
            self.thin_arc_end_angle %= 360
            self.thin_arc_end_angle -= 360

        if self.thick_arc_start_angle >= 3600:
            self.thick_arc_start_angle %= 360
            self.thick_arc_start_angle += 360

        elif self.thick_arc_start_angle <= -3600:
            self.thick_arc_start_angle %= 360
            self.thick_arc_start_angle -= 360

        if self.thick_arc_end_angle >= 3600:
            self.thick_arc_end_angle %= 360
            self.thick_arc_end_angle += 360

        elif self.thick_arc_end_angle <= -3600:
            self.thick_arc_end_angle %= 360
            self.thick_arc_end_angle -= 360

    def rotate_arcs(self):
        """The low-level method to rotating the arcs.
        """

        if self.arc_direction:
            self.thick_arc_start_angle -= 5
            self.thick_arc_end_angle -= 5

            self.thin_arc_start_angle += 5
            self.thin_arc_end_angle += 5
        else:
            self.thick_arc_start_angle += 5
            self.thick_arc_end_angle += 5

            self.thin_arc_start_angle -= 5
            self.thin_arc_end_angle -= 5
