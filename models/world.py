import numpy as np
from PIL import Image
# from pynput.mouse import Controller

from models.Sphere import Sphere
from models.face import Face
from models.vertex import Vertex
from ray import Ray
from util.Util import Util


class World(object):
    def __init__(self, camera, light_source_point):
        self.camera = camera
        self.objects = []
        self.light_source_point = light_source_point
        self.ILLU_INTENSITY_CONST = 700

    def add_object(self, td_object):
        self.objects.append(td_object)

    def render(self):
        h = self.camera.canvas_resolution[0]
        w = self.camera.canvas_resolution[0]
        data = np.zeros((h, w, 3), dtype=np.uint8)
        iteration = 3
        # while (True):
        try:
            for x in range(self.camera.canvas_resolution[0]):
                for y in range(self.camera.canvas_resolution[1]):
                    xcor, ycor = self.camera.get_pixel_coordinates(x, y)
                    ray = Ray(0, 0, 0, self)
                    r, g, b = ray.render_pixel(np.array([xcor, ycor, self.camera.canvas_dist]))
                    data[y, x] = [r, g, b]
                    print(f'Rendered pixel [y,x]: [{y},{x}] with [r,g,b] : [{r},{g},{b}]')
                if iteration % 20 == 0:
                    img = Image.fromarray(data, 'RGB')
                    img.save(f"progression_int/first_{iteration}.png")
                iteration += 1
            # mp = mouse.position
            # shift_x = (mp[0] - mx) / 10
            # shift_y = (mp[1] - my) / 10
            # print(shift_x,shift_y)
            # self.td_objects[0].centre = Vertex(shift_x, shift_y, 15)
            # iteration += 1
        except KeyboardInterrupt as ke:
            print('Terminating...', ke)

    # def hit_obstacle(self, xray, yray, zray):
    #     zdiff = self.td_objects[0].centre.zc() - zray
    #     if zdiff < 0:
    #         zdiff = zdiff * -1
    #     if zdiff < 1 \
    #             and self.td_objects[0].r > \
    #             Util.get_distance_between_two_3d_points(self.td_objects[0].centre, Vertex(xray, yray, zray)):
    #         return True, self.td_objects[0]
    #     return False, None

    def hit_obstacle(self, xray, yray, zray):
        for td_object in self.objects:
            if isinstance(td_object,Sphere):
                if Util.get_distance_between_two_3d_points(td_object.centre, Vertex(xray, yray, zray)) <= td_object.radius:
                    return True, td_object
            if isinstance(td_object,Face):
                return True, td_object
        return False, None
