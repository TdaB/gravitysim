import logging
from gravity_equations import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

__all__ = ['MassiveObject']


class MassiveObject(object):
    def __init__(self, mass, radius, center_x, center_y, v_x, v_y, color):
        self.timestep = .01 # seconds
        self.mass = mass
        self.x = center_x
        self.y = center_y
        self.radius = radius
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = 0
        self.a_y = 0
        self.t = 0
        self.color = color
        #self.is_deleted = False
        logger.info("Creating %s at (%s, %s)" % (self.color, self.x, self.y))

    def __eq__(self, m):
        return self.x == m.x and self.y == m.y

    def __str__(self):
        to_return = ""
        to_return += "Color = " + self.color + '\n'
        to_return += "t = " + str(self.t) + '\n'
        to_return += "x = " + str(self.x) + '\n'
        to_return += "y = " + str(self.y) + '\n'
        to_return += "v_x = " + str(self.v_x) + '\n'
        to_return += "v_y = " + str(self.v_y) + '\n'
        to_return += "a_x = " + str(self.a_x) + '\n'
        to_return += "a_y = " + str(self.a_y) + '\n'
        return to_return
