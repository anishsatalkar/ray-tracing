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

    def render_pixel(self, point_on_line_point):
        object_reference = None
        illumination_intensity = None
        for initial_intersection_object in self.world.objects:
            illumination_intensity = None
            object_reference = initial_intersection_object
            if initial_intersection_object.type == 'sphere':
                initial_intersection_closest_point, initial_intersection_farthest_point = \
                    self._handle_sphere_intersection(
                        point_on_line_point,
                        np.array([0, 0, 0]),
                        initial_intersection_object)
                if initial_intersection_closest_point is not None:
                    illumination_intensity = self._cast_shadow_rays(initial_intersection_closest_point,
                                                                    initial_intersection_object)
                    break
            elif initial_intersection_object.type == 'plane':
                pass
            else:
                print(f'Skipping object {initial_intersection_object} since its not a sphere or a plane')
        if illumination_intensity:
            return min(255, object_reference.colour[0] * illumination_intensity), \
                   min(255, object_reference.colour[1] * illumination_intensity), \
                   min(255, object_reference.colour[2] * illumination_intensity)
            # return 250, 250, 250
        return 0, 0, 0

    def begin(self, xcor, ycor, zcor):
        xd, yd, zd = self._get_component_deltas(xcor, ycor, zcor)
        P = np.array([xcor, ycor, zcor])
        vector_along_pixel = np.array([xcor, ycor, zcor]) - np.array([self.x, self.y, self.z])
        U = vector_along_pixel / (vector_along_pixel ** 2).sum() ** 0.5
        iterations = 0
        # color = (224, 236, 255)
        color = BaseObject.BLACK
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

    def _handle_sphere_intersection(self, line_on_point, ray_start_point, obj):
        C = np.array([obj.centre.xc(), obj.centre.yc(), obj.centre.zc()])
        r = obj.radius
        P = line_on_point
        vector_along_pixel = line_on_point - ray_start_point
        U = vector_along_pixel / (vector_along_pixel ** 2).sum() ** 0.5

        Q = P - C
        a = np.dot(U, U)
        b = 2 * np.dot(U, Q)
        c = np.dot(Q, Q) - r * r
        d = b * b - 4 * a * c
        if d >= 0:
            roots = np.roots([a, b, c])
            r1, r2 = roots[0], roots[1]
            # if r1 >= 0: TODO Can this be used for intersections behind the sphere in the case of shadow rays?
            poi_1 = P + r1 * U
            dist_poi_1 = np.linalg.norm(poi_1 - line_on_point)
            # if r2 >= 0: TODO Can this be used for intersections behind the sphere in the case of shadow rays?
            poi_2 = P + r2 * U
            dist_poi_2 = np.linalg.norm(poi_2 - line_on_point)

            # print(f'Intersects for pixel {line_on_point}, Point 1 : {poi_1},  '
            #       f'Point 2 : {poi_2} Dist poi_1 : {dist_poi_1} Dist poi_2 : {dist_poi_2}')
            if dist_poi_1 and dist_poi_2:
                return (poi_1, poi_2) if dist_poi_1 <= dist_poi_2 else (poi_2, poi_1)
            elif dist_poi_1 and not dist_poi_2:
                return poi_1, None
            elif dist_poi_2 and not dist_poi_1:
                return poi_2, None
            else:
                return None, None
        else:
            return None, None

    def _handle_plane_intersection(self, xcor, ycor, zcor, obj):
        pass

    def _cast_shadow_rays(self, initial_ray_intersection_point, initial_intersection_object):
        for shadow_ray_object in self.world.objects:
            if shadow_ray_object.type == 'sphere':
                shadow_ray_intersection_closest_point, shadow_ray_intersection_farthest_point = \
                    self._handle_sphere_intersection(self.world.light_source_point, initial_ray_intersection_point,
                                                     shadow_ray_object)
                if shadow_ray_object == initial_intersection_object:
                    if not np.allclose(shadow_ray_intersection_closest_point, initial_ray_intersection_point):
                        return None
                else:
                    if shadow_ray_intersection_closest_point is not None and shadow_ray_intersection_closest_point.any():
                        if Ray._is_intersection_between_two_points(initial_ray_intersection_point,
                                                                   shadow_ray_intersection_closest_point,
                                                                   shadow_ray_intersection_farthest_point,
                                                                   self.world.light_source_point):
                            return None
                            # pass
        return self._get_light_intensity(initial_ray_intersection_point)

    def _get_light_intensity(self, intersection_point):
        return self.world.ILLU_INTENSITY_CONST / np.linalg.norm(self.world.light_source_point - intersection_point)

    @staticmethod
    def _is_intersection_between_two_points(initial_ray_intersection_point,
                                            shadow_ray_intersection_closest_point,
                                            shadow_ray_intersection_farthest_point,
                                            light_source_point):
        if not shadow_ray_intersection_closest_point.any():
            raise Exception('Ray must intersect')
        initial_intersection_lightsource_distance = np.linalg.norm(light_source_point - initial_ray_intersection_point)
        shadow_ray_intersection_distance = np.linalg.norm(light_source_point - shadow_ray_intersection_closest_point)
        if shadow_ray_intersection_distance < initial_intersection_lightsource_distance:
            return True
        return False
