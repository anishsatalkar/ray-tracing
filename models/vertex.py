class Vertex(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def xc(self):
        return self.x

    def yc(self):
        return self.y

    def zc(self):
        return self.z

    @classmethod
    def x_diff(cls, vertex2, vertex1):
        # TODO Use distance in 2D formula
        return vertex2.xc() - vertex1.xc()

    @classmethod
    def y_diff(cls, vertex2, vertex1):
        # TODO Use distance in 2D formula
        return vertex2.yc() - vertex1.yc()

    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
