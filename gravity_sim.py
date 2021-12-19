import logging
from tkinter import Tk, Canvas
from random import randint, choice
from physics import *
from massive_object import *
from colors import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

TIMESTEP = .01  # seconds


class Simulator(object):
    def __init__(self):
        tk = Tk()
        tk.title = "T da B's Gravity Simulator"
        self.width = 1920
        self.height = 1080
        self.canvas = Canvas(tk, width=self.width, height=self.height, bg='black')
        self.masses = list()
        self.init_masses()
        self.canvas.pack()
        self.draw()
        tk.mainloop()

    def init_masses(self):
        for _ in range(20):
            size = randint(3, 7)
            m = MassiveObject(
                size * 10 ** 12,
                size,
                randint(100, self.width - 100),
                randint(100, self.height - 100),
                randint(-15, 15),
                randint(-15, 15),
                random_color()
            )
            m.canvas_id = self.canvas.create_oval(m.x - m.radius,
                                                  m.y - m.radius,
                                                  m.x + m.radius,
                                                  m.y + m.radius,
                                                  outline=m.color,
                                                  fill=m.color)
            self.masses.append(m)

    def draw(self):
        """
        Main loop
        """
        for m in self.masses:
            # if m.is_deleted is True:
            #    self.masses.remove(m)
            #    continue
            for m2 in self.masses:
                if m2 == m:
                    continue
                else:
                    self.update(m, m2)
            #self.draw_accel_vector(m)
            self.draw_vel_vector(m)
        self.canvas.after(10, self.draw)

    def update(self, m1, m2):
        """
        Update MassiveObject m1 with respect to m2
        """
        # if ( distance(m1, m2) < m1.radius + m2.radius ):
        #    logger.info("%s and %s collided!" % (m1.color, m2.color))
        #    self.canvas.delete(m1.canvas_id, m2.canvas_id)

        #    text = self.canvas.create_text((m1.x + m2.x) / 2,
        #                                 (m1.y + m2.y) / 2,
        #                                 text="COLLISION!",
        #                                 fill='red')
        #    self.canvas.after(1000, self.canvas.delete, text)
        #    m1.is_deleted = True
        #    m2.is_deleted = True
        if distance(m1.x, m1.y, m2.x, m2.y) <= m1.radius + m2.radius:
            # text = self.canvas.create_text((m1.x + m2.x) / 2,
            #                              (m1.y + m2.y) / 2,
            #                              text="COLLISION!",
            #                              fill='red')
            # self.canvas.after(1000, self.canvas.delete, text)
            m1.v_x, m2.v_x = elastic_headon_collision(m1.mass, m1.v_x, m2.mass, m2.v_x)
            m1.v_y, m2.v_y = elastic_headon_collision(m1.mass, m1.v_y, m2.mass, m2.v_y)
            return

        old_x = m1.x
        old_y = m1.y
        g_x, g_y = grav_force(m1, m2)
        m1.a_x = g_x / m1.mass
        m1.a_y = g_y / m1.mass
        m1.x += TIMESTEP * (m1.v_x + .5 * (TIMESTEP * m1.a_x))
        m1.y += TIMESTEP * (m1.v_y + .5 * (TIMESTEP * m1.a_y))
        g_x, g_y = grav_force(m1, m2)
        new_a_x, new_a_y = g_x / m1.mass, g_y / m1.mass
        m1.v_x += TIMESTEP * .5 * (m1.a_x + new_a_x)
        m1.v_y += TIMESTEP * .5 * (m1.a_y + new_a_y)

        self.canvas.move(m1.canvas_id, m1.x - old_x, m1.y - old_y)
        logger.info("Updated %s from (%s, %s) to (%s, %s)" % (m1.color, old_x, old_y, m1.x, m1.y))

    def draw_accel_vector(self, m):
        mag = distance(m.x, m.y, m.x + m.a_x, m.y + m.a_y)
        if mag > 1:
            line = self.canvas.create_line(m.x,
                                           m.y,
                                           m.x + m.a_x,
                                           m.y + m.a_y,
                                           fill='yellow',
                                           arrow='last')

            text = self.canvas.create_text(m.x + 1.2 * m.a_x,
                                           m.y + 1.2 * m.a_y,
                                           text=str(int(mag)),
                                           fill='yellow')
            self.canvas.after(int(TIMESTEP * 1000), self.canvas.delete, line, text)

    def draw_vel_vector(self, m):
        mag = distance(m.x, m.y, m.x + m.v_x, m.y + m.v_y)
        if mag > 1:
            line = self.canvas.create_line(m.x,
                                           m.y,
                                           m.x + m.v_x,
                                           m.y + m.v_y,
                                           fill='red',
                                           arrow='last')

            text = self.canvas.create_text(m.x + 1.2 * m.v_x,
                                           m.y + 1.2 * m.v_y,
                                           text=str(int(mag)),
                                           fill='red')
            self.canvas.after(int(TIMESTEP * 1000), self.canvas.delete, line, text)


if __name__ == '__main__':
    Simulator()
