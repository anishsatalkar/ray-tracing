from random import randrange

import numpy as np

from models.BaseObject import BaseObject
from util.Util import Util


class Ray(object):
    def __init__(self, x, y, z, world):
        self.x = x
        self.y = y
        self.z = z
        self.world = world
        self.hit_count = 0

    def hit(self):
        pass

    def begin(self, xcor, ycor, zcor):
        xd, yd, zd = self._get_component_deltas(xcor, ycor, zcor)
        P = np.array([xcor, ycor, zcor])
        vector_along_pixel = np.array([xcor, ycor, zcor]) - np.array([self.x, self.y, self.z])
        U = vector_along_pixel / (vector_along_pixel **2).sum() ** 0.5
        iterations = 0
        # color = (224, 236, 255)
        color = BaseObject.DARK_GRAY
        while iterations <= 50 and self.hit_count < 3:
            has_hit_obstacle, td_object = self.world.hit_obstacle(self.x, self.y, self.z)
            if has_hit_obstacle:
                self.hit_count += 1
                print(f"Just hit {td_object} at {self.x, self.y, self.z}. Total hits so far {self.hit_count}")
                if td_object.is_light_source:
                    return td_object.colour
                else:
                    d = np.array([self.x, self.y, self.z])
                    n = d - np.array([td_object.centre.xc(), td_object.centre.yc(), td_object.centre.zc()])
                    r = self._get_reflection_vector(d, n, td_object)
                    # r = d - 2 * (np.dot(d, n)) * (n / np.sqrt(np.sum(n**2)))
                    r = r / np.sqrt(np.sum(r ** 2))
                    xd, yd, zd = r[0], r[1], r[2]

                    # TODO : Here the color of object is returned as it is. This should actually be a combination of
                    #   other factors as well. Otherwise the object lits up evenly at every point and shadows are
                    #   missed completely.
                    color = td_object.colour
            self.x += xd
            self.y += yd
            self.z += zd
            iterations += 1
        if self.hit_count == 2:
            print('second hit')
        if self.hit_count > 0:
            return color
        return color

        pass

    def _get_component_deltas(self, xcor, ycor, zcor):
        xdiff = xcor - self.x
        ydiff = ycor - self.y
        zdiff = zcor - self.z

        base_hypo = Util.get_hypotenuse_distance(xdiff, zdiff)
        three_d_hypo = Util.get_hypotenuse_distance(base_hypo, ydiff)
        sin_y = ydiff / three_d_hypo
        cos_y = base_hypo / three_d_hypo

        y_to_travel = 1 * sin_y

        cos_x = xdiff / base_hypo
        x_to_travel = 1 * cos_x

        cos_z = zdiff / base_hypo
        z_to_travel = 1 * cos_z
        return x_to_travel, y_to_travel, z_to_travel

    def _get_reflection_vector(self, d, n, td_object):
        if td_object.material == "reflective":
            return d - 2 * (np.dot(d, n)) * (n / np.sqrt(np.sum(n ** 2)))
        else:
            return (d - 2 * (np.dot(d, n)) * (n / np.sqrt(np.sum(n ** 2)))) + randrange(-5, 5)
