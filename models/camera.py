from models.vertex import Vertex


class Camera(object):
    def __init__(self, vantage_pt, canvas_dist, canvas_face, canvas_resolution):
        self.vantage_pt = vantage_pt
        self.canvas_dist = canvas_dist
        self.canvas_face = canvas_face
        self.canvas_resolution = canvas_resolution
        self._xdiff = Vertex.x_diff(self.canvas_face.vertices[2], self.canvas_face.vertices[1])
        self._ydiff = Vertex.y_diff(self.canvas_face.vertices[2], self.canvas_face.vertices[3])
        self.x_pixel_width = self._xdiff / canvas_resolution[0]
        self.y_pixel_width = self._ydiff / canvas_resolution[1]

    def get_pixel_coordinates(self, x_pixel: float, y_pixel: float) -> (float,float):
        xv = self.canvas_face.vertices[0].xc()
        yv = self.canvas_face.vertices[0].yc()
        xcor = (self.x_pixel_width * (x_pixel + 1)) - (self.x_pixel_width * 0.5) + xv
        ycor = (self.y_pixel_width * (y_pixel + 1)) - (self.y_pixel_width * 0.5) + yv
        return xcor,ycor

