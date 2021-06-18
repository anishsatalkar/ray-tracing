import math


class Util(object):
    def __init__(self):
        pass

    @staticmethod
    def get_hypotenuse_distance(a, b):
        return math.sqrt(a * a + b * b)

    @staticmethod
    def get_distance_between_two_3d_points(vertex1, vertex2):
        return math.sqrt((vertex1.xc() - vertex2.xc()) ** 2 +
                         (vertex1.yc() - vertex2.yc()) ** 2 +
                         (vertex1.zc() - vertex2.zc()) ** 2)
