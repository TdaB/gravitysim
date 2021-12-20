import logging
from tkinter import Tk, Canvas
from random import randint
from physics import *
from massive_object import *
from colors import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
config = configparser.ConfigParser()
config.read('../config.ini')
window_width = config.getint('DEFAULT', 'window.width')
window_height = config.getint('DEFAULT', 'window.height')
draw_refresh = config.getint('DEFAULT', 'draw.refresh.ms')
seconds_per_frame = config.getint('DEFAULT', 'seconds.per.frame')
meters_per_pixel = config.getint('DEFAULT', 'meters.per.pixel')


class Simulator(object):
    def __init__(self):
        tk = Tk()
        tk.title = "T da B's Gravity Simulator"
        self.canvas = Canvas(tk,
                             width=window_width,
                             height=window_height,
                             bg='black')
        self.masses = list()
        self.init_masses()
        self.canvas.pack()
        self.draw()
        tk.mainloop()

    def init_masses(self):
        for _ in range(50):
            mass_multiplier = randint(1, 30)
            radius_multiplier = randint(1, 50)
            m = MassiveObject(
                mass_multiplier * 2 * 10 ** 30,
                radius_multiplier * 700 * 10 ** 6,
                randint(100, window_width - 100),
                randint(100, window_height - 100),
                randint(-15, 15),
                randint(-15, 15),
                random_color()
            )
            scaled_radius = m.radius / meters_per_pixel
            m.canvas_id = self.canvas.create_oval(m.x - scaled_radius,
                                                  m.y - scaled_radius,
                                                  m.x + scaled_radius,
                                                  m.y + scaled_radius,
                                                  outline=m.color,
                                                  fill=m.color)
            self.masses.append(m)

    def draw(self):
        """
        Main loop
        """
        for m in self.masses:
            for m2 in self.masses:
                if m2 == m:
                    continue
                else:
                    self.update(m, m2)
            # self.draw_accel_vector(m)
            # self.draw_vel_vector(m)
        self.canvas.after(draw_refresh, self.draw)

    def update(self, m1, m2):
        d = distance(m1.x, m1.y, m2.x, m2.y)
        if d < m1.radius + m2.radius:
            self.separate(m1, m2, d)
            m1.v_x, m2.v_x = elastic_headon_collision(m1.mass, m1.v_x, m2.mass, m2.v_x)
            m1.v_y, m2.v_y = elastic_headon_collision(m1.mass, m1.v_y, m2.mass, m2.v_y)
            return
        old_x = m1.x
        old_y = m1.y
        old_a_x = m1.a_x
        old_a_y = m1.a_y
        m1.x += seconds_per_frame * (m1.v_x + .5 * (seconds_per_frame * m1.a_x)) / meters_per_pixel
        m1.y += seconds_per_frame * (m1.v_y + .5 * (seconds_per_frame * m1.a_y)) / meters_per_pixel
        g_x, g_y = grav_force(m1, m2, d)
        m1.a_x = g_x / m1.mass
        m1.a_y = g_y / m1.mass
        m1.v_x += seconds_per_frame * .5 * (m1.a_x + old_a_x)
        m1.v_y += seconds_per_frame * .5 * (m1.a_y + old_a_y)

        self.canvas.move(m1.canvas_id, m1.x - old_x, m1.y - old_y)
        logger.info("Updated %s from (%s, %s) to (%s, %s)" % (m1.color, old_x, old_y, m1.x, m1.y))

    def separate(self, m1, m2, d):
        separation_d = m1.radius + m2.radius - d
        pixel_d = .5 * separation_d / meters_per_pixel

        unit_x, unit_y = unit_vector(m1.x - m2.x, m1.y - m2.y)
        new_x = m1.x + pixel_d * unit_x
        new_y = m1.y + pixel_d * unit_y
        self.canvas.move(m1.canvas_id, new_x - m1.x, new_y - m1.y)
        m1.x = new_x
        m1.y = new_y

        unit_x, unit_y = -unit_x, -unit_y
        new_x = m2.x + pixel_d * unit_x
        new_y = m2.y + pixel_d * unit_y
        self.canvas.move(m2.canvas_id, new_x - m2.x, new_y - m2.y)
        m2.x = new_x
        m2.y = new_y


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
            self.canvas.after(draw_refresh, self.canvas.delete, line, text)

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
            self.canvas.after(draw_refresh, self.canvas.delete, line, text)


if __name__ == '__main__':
    Simulator()
