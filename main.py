import numpy as np

from models.BaseObject import BaseObject
from models.Sphere import Sphere
from models.camera import Camera
from models.face import Face
from models.vertex import Vertex
from models.world import World

if __name__ == '__main__':
    world = World(
        Camera(
            vantage_pt=Vertex(0, 0, 0),
            canvas_dist=5,
            canvas_face=Face(Vertex(0, 0, 5), 4, 0, 0, 0),
            canvas_resolution=(400, 400)
        ),
        np.array([25, 0, 0])
    )

    # world.add_object(Face(Vertex(0,0,15), 2, 0, 0, 0))
    # world.add_object(Circle(Vertex(3, 3, 15), 2, 0, 0, 0))
    # world.add_object(Sphere(Vertex(-5, 0, 15), 1, BaseObject.BLUE, False, BaseObject.REFLECTIVE))
    world.add_object(Sphere(Vertex(0, 0, 40), 7, BaseObject.BLUE, False, BaseObject.DIFFUSE))
    world.add_object(Sphere(Vertex(5, 0, 25), 2, BaseObject.ORANGE, False, BaseObject.DIFFUSE))
    # world.add_object(Sphere(Vertex(-3, 5, 15), 2, BaseObject.ORANGE, True, BaseObject.REFLECTIVE))
    # world.add_object(Sphere(Vertex(0, 0, 15), 2, BaseObject.BLUE, False))
    # world.add_object(Sphere(Vertex(-2, -2, 16), 1, BaseObject.WHITE, False))
    # world.add_object(Sphere(Vertex(-3, -4, 13), 1, BaseObject.ORANGE, True))
    # world.add_object(Sphere(Vertex(3, 0, 11), 1, [255, 255, 255], True))

    # world.add_object(Sphere(Vertex(0, 3, 12), 1, BaseObject.WHITE, True))
    # world.add_object(Sphere(Vertex(0, -3, 12), 1, [255, 255, 255], True))
    # world.add_object(Sphere(Vertex(3.5, 0, 10), 1, BaseObject.WHITE, True))
    # world.add_object(Sphere(Vertex(-3, 0, 12), 1, [255, 255, 255], True))

    world.render()
