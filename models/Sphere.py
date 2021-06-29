from models.BaseObject import BaseObject
from models.vertex import Vertex


class Sphere(BaseObject):
    def __init__(self, vertex: Vertex, radius: float, colour: list, is_light_source: bool, material=BaseObject.REFLECTIVE):
        super().__init__(colour)
        self.centre = vertex
        self.radius = radius
        self.is_light_source = is_light_source
        self.material = material
        self.type = BaseObject.SPHERE

    def __str__(self):
        return f"[{self.__class__}, centre={self.centre}, r={self.radius}, is_light_source={self.is_light_source}]"