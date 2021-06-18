from models.vertex import Vertex


class Face(object):
    def __init__(self, vertex, len, xr, yr, zr):
        self.vertices = self.get_vertices_from_central_vertex(vertex, len)

    def get_vertices_from_central_vertex(self, vertex, len):
        vertex_1 = Vertex(vertex.xc() - len / 2,
                          vertex.yc() - len / 2,
                          vertex.zc())

        vertex_2 = Vertex(vertex.xc() - len / 2,
                          vertex.yc() + len / 2,
                          vertex.zc())

        vertex_3 = Vertex(vertex.xc() + len / 2,
                          vertex.yc() + len / 2,
                          vertex.zc())

        vertex_4 = Vertex(vertex.xc() + len / 2,
                          vertex.yc() - len / 2,
                          vertex.zc())

        return [vertex_1,vertex_2,vertex_3,vertex_4]
