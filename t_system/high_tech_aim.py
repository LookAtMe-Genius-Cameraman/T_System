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


class Aimer:
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

        self.rect_diagonal_rate = 0.9

    def mark_rotating_arcs(self, image, center, radius, physically_distance, color='red'):
        """The top-level method to draw target mark with rotating arcs like high tech.

        Args:
                image:       	        Image matrix.
                center:       	        Center point of the aimed object.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
                color:                  The dominant color of the targeting mark.
        """
        self.image = image
        self.object_distance = str(round(physically_distance * 0.164 / 1000, 2)) + " m"  # 0.164 mm is the length of one pixel.

        radius *= 0.618
        thickness = radius * 0.23
        self.image_height, self.image_width = self.image.shape[:2]

        center_x = center[0]
        center_y = center[1]

        self.draw_arc(center_x, center_y, radius, thickness, self.thick_arc_start_angle, self.thick_arc_end_angle)
        self.draw_arc(center_x, center_y, radius * 0.95, thickness * 0.15, self.thin_arc_start_angle, self.thin_arc_end_angle)

        text_point = (int(center_x - radius * 0.15), int(center_y + radius * 0.95 - radius * 0.1))

        # parameters: image, put text, text's coordinates,font, scale, color, thickness, line type(this type is best for texts.)
        cv2.putText(self.image, self.object_distance, text_point, self.text_font, radius * 0.004, (0, 0, 200), int(radius * 0.004), cv2.LINE_AA)

        self.draw_phys_dist_container(center_x, center_y, radius)

        self.check_angle_of_arcs()
        self.rotate_arcs()

        return self.image

    def mark_parital_rect(self, image, center, radius, physically_distance, color='red'):
        """The top-level method to draw target mark with partial rectangle like high tech.

        Args:
                image:       	        Image matrix.
                center:       	        Center point of the aimed object.
                radius:                 Radius of the aim.
                physically_distance:    Physically distance of the targeted object as pixel count.
        """

        self.image = image
        self.object_distance = str(round(physically_distance * 0.164 / 1000, 2)) + " m"  # 0.164 mm is the length of one pixel.

        radius *= 0.5
        thickness = radius * 0.23
        self.image_height, self.image_width = self.image.shape[:2]

        center_x = center[0]
        center_y = center[1]

        self.draw_rect(center_x, center_y, radius * 1.2, thickness * 0.4)
        # self.draw_rect_triangler(center_x, center_y, radius * self.rect_diagonal_rate, thickness * 0.2)

        text_point = (int(center_x - radius * 0.15), int(center_y + radius * 0.95 - radius * 0.1))

        cv2.putText(self.image, self.object_distance, text_point, self.text_font, radius * 0.004, (0, 200, 0), int(radius * 0.004), cv2.LINE_AA)
        # parameters: image, put text, text's coordinates,font, scale, color, thickness, line type(this type is best for texts.)

        # self.rect_diagonal_rate -= 0.05
        # if self.rect_diagonal_rate <= 0.2:
        #     self.rect_diagonal_rate = 0.9

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
                    distance = int(sqrt((center_x - x) ** 2 + (center_y - y) ** 2))
                    x = int(x)
                    y = int(y)
                    if radius <= distance <= radius + thickness:
                        [b, g, r] = self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, 0, 1.1])

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
                                    self.image[y, x] = numpy.array(self.image[y, x]) + numpy.array([thick * 0.06, thick * 0.06, 255])
                angle += 0.25
            rad += 1

    def draw_rect(self, center_x, center_y, radius, thickness):
        """The low-level method to draw partial rectangles those have missing parts of their edges.

        Args:
                center_x:       	  The object's x center(by column count).
                center_y:             The object's y center(by row count).
                radius:               Radius of the aim.
                thickness:            Thickness of arc.
        """

        center_x = int(center_x)
        center_y = int(center_y)
        radius = int(radius)
        thickness = int(thickness)

        edge_length = int(radius * 0.3)

        x_ranges = list(range(center_x - radius - thickness, center_x - edge_length)) + list(range(center_x + edge_length, center_x + radius + thickness))
        y_ranges = list(range(center_y - radius - thickness, center_y - radius)) + list(range(center_y + radius, center_y + radius + thickness))

        for x in x_ranges:
            for y in y_ranges:

                if self.image_width > x >= 0 and self.image_height > y >= 0:  # for the frames' limit protection.
                    [b, g, r] = self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, 1, 0])

                    if g <= 100:
                        if g == 0:
                            g = 1
                            self.image[y, x] = [0, 0, 1]
                        greenness_rate = (255 / g) / 0.12
                        self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, greenness_rate, 0])

        y_ranges = list(range(center_y - radius - thickness, center_y - edge_length)) + list(range(center_y + edge_length, center_y + radius + thickness))
        x_ranges = list(range(center_x - radius - thickness, center_x - radius)) + list(range(center_x + radius, center_x + radius + thickness))

        for y in y_ranges:
            for x in x_ranges:

                if self.image_width > x >= 0 and self.image_height > y >= 0:  # for the frames' limit protection.
                    [b, g, r] = self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, 1, 0])

                    if g <= 100:
                        if g == 0:
                            g = 1
                            self.image[y, x] = [0, 0, 1]
                        greenness_rate = (255 / g) / 0.12
                        self.image[y, x] = numpy.array(self.image[y, x]) * numpy.array([0, greenness_rate, 0])

        x_ranges = list(range(int(center_x - radius * 1.5), int(center_x - edge_length))) + list(range(int(center_x + edge_length), int(center_x + radius * 1.5)))

        for x in x_ranges:
            if self.image_width > x >= 0:  # for the frames' limit protection.
                self.image[center_y, x] = numpy.array(self.image[center_y, x]) * numpy.array([0, 2, 0])

        y_ranges = list(range(int(center_y - radius * 1.5), int(center_y - edge_length))) + list(range(int(center_y + edge_length), int(center_y + radius * 1.5)))

        for y in y_ranges:
            if self.image_height > y >= 0:  # for the frames' limit protection.
                self.image[y, center_x] = numpy.array(self.image[y, center_x]) * numpy.array([0, 2, 0])

    def draw_phys_dist_container(self, center_x, center_y, radius):
        """The low-level method to draw the trapezoid shape for the container of physically distance value.
        """

        dis_con_point_1 = int(center_x - radius * 0.95 * sin(radians(15))), int(center_y + radius * 0.95 * cos(radians(45)))
        dis_con_point_2 = int(center_x + radius * 0.95 * sin(radians(15))), int(center_y + radius * 0.95 * cos(radians(45)))
        dis_con_point_3 = int(center_x + radius * 0.95 * sin(radians(20))), int(center_y + radius * 0.95 * cos(radians(15)))
        dis_con_point_4 = int(center_x - radius * 0.95 * sin(radians(20))), int(center_y + radius * 0.95 * cos(radians(15)))

        cv2.line(self.image, dis_con_point_1, dis_con_point_2, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.line(self.image, dis_con_point_2, dis_con_point_3, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.line(self.image, dis_con_point_1, dis_con_point_4, (0, 0, 255), 1, cv2.LINE_AA)

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
