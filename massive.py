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
    def __init__(self, canvas, mass, radius, center_x, center_y, v_x, v_y, color):
        self.timestep = .01 # seconds
        self.canvas = canvas
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
        self.is_deleted = False
        self.canvas_id = canvas.create_oval(self.x - self.radius,
                                            self.y - self.radius,
                                            self.x + self.radius,
                                            self.y + self.radius,
                                            outline=color,
                                            fill=color)
        logger.info("Creating %s at (%s, %s)" % (self.color, self.x, self.y))

    def update(self, p):
        #print "Updating %s..." % self.color
        #print self
        if ( distance(self, p) < self.radius + p.radius ):
            logger.info("%s and %s collided!" % (self.color, p.color))
            self.canvas.delete(self.canvas_id, p.canvas_id)

            text = self.canvas.create_text((self.x + p.x) / 2,
                                           (self.y + p.y) / 2,
                                           text="COLLISION!",
                                           fill='red')
            self.canvas.after(1000, self.canvas.delete, text)
            self.is_deleted = True
            p.is_deleted = True
        old_x = self.x
        old_y = self.y
        g_x, g_y = grav_force(self, p)
        self.a_x = g_x / self.mass
        self.a_y = g_y / self.mass
        self.t += self.timestep
        self.x += self.timestep * (self.v_x + .5*(self.timestep * self.a_x))
        self.y += self.timestep * (self.v_y + .5*(self.timestep * self.a_y))
        g_x, g_y = grav_force(self, p)
        new_a_x, new_a_y = g_x / self.mass, g_y / self.mass
        self.v_x += self.timestep * .5 * (self.a_x + new_a_x)
        self.v_y += self.timestep * .5 * (self.a_y + new_a_y)

        #print self
        
        self.canvas.move(self.canvas_id, self.x - old_x, self.y - old_y)
        logger.info("Updated %s from (%s, %s) to (%s, %s)" % (self.color, old_x, old_y, self.x, self.y))

    def draw_accel_vector(self):
        m = mag(self.x, self.y, self.x + self.a_x, self.y + self.a_y)
        if m > 1:
            line = self.canvas.create_line(self.x,
                                           self.y,
                                           self.x + self.a_x,
                                           self.y + self.a_y,
                                           fill='yellow',
                                           arrow='last')

            text = self.canvas.create_text(self.x + 1.2 * self.a_x,
                                           self.y + 1.2 * self.a_y,
                                           text=str(int(m)),
                                           fill='yellow')
            self.canvas.after(int(self.timestep * 1000), self.canvas.delete, line, text)

    def draw_vel_vector(self):
        m = mag(self.x, self.y, self.x + self.v_x, self.y + self.v_y)
        if m > 1:
            line = self.canvas.create_line(self.x,
                                           self.y,
                                           self.x + self.v_x,
                                           self.y + self.v_y,
                                           fill='red',
                                           arrow='last')

            text = self.canvas.create_text(self.x + 1.2 * self.v_x,
                                           self.y + 1.2 * self.v_y,
                                           text=str(int(m)),
                                           fill='red')
            self.canvas.after(int(self.timestep * 1000), self.canvas.delete, line, text)


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

