class BaseObject(object):
    WHITE = [255, 255, 255]
    BLUE = [2, 114, 199]
    ORANGE = [235, 125, 52]
    GREEN = [182, 222, 40]
    DARK_GRAY = [105, 105, 105]
    BLACK = [10, 10, 10]

    REFLECTIVE = 'reflective'
    DIFFUSE = 'diffuse'

    SPHERE = 'sphere'
    PLANE = 'plane'

    def __init__(self, colour: list):
        self.colour = colour
