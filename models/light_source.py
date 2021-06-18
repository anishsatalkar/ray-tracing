from models.BaseObject import BaseObject


class LightSource(BaseObject):
    def __init__(self, colour: list):
        super().__init__(colour)
