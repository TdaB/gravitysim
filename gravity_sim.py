import logging
from Tkinter import Tk, Canvas
from random import randint, choice
from gravity_equations import *
from massive import *

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

TIMESTEP = .01 # seconds


def random_color():
    """
    Returns a random color in the format: '#abc123'
    """
    choices = [str(n) for n in range(9)] + [c for c in 'abcdef']
    result = '#'
    for _ in range(6):
        result += choice(choices)
    return result


def avg_color(c1, c2):
    """
    Returns the average of two colors
    """
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r, g, b = int(round((r1 + r2) / 2)), int(round((g1 + g2) / 2)), int(round((b1 + b2) / 2))
    result = '#' + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]
    return result


class Simulator(object):
    def __init__(self):
        tk=Tk()
        tk.title = "T da B's Gravity Simulator"
        self.width = 1900
        self.height = 1000

        self.canvas=Canvas(tk, width=self.width, height=self.height, bg='black')
        self.masses = list()
        for _ in range(10):
            size = randint(3, 7)
            m = MassiveObject(
                size * 10**16,
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
        self.canvas.pack()

        self.draw()
        tk.mainloop()

    def draw(self):
        """
        Main loop
        """
        for m in self.masses:
            #if m.is_deleted is True:
            #    self.masses.remove(m)
            #    continue
            for m2 in self.masses:
                if m2 == m:
                    continue
                else:
                    self.update(m, m2)
            #m.draw_accel_vector()
            #m.draw_vel_vector()
        self.canvas.after(10, self.draw)

    def update(self, m1, m2):
        """
        Update MassiveObject m1 with respect to m2
        """
        #if ( distance(m1, m2) < m1.radius + m2.radius ):
        #    logger.info("%s and %s collided!" % (m1.color, m2.color))
        #    self.canvas.delete(m1.canvas_id, m2.canvas_id)

        #    text = self.canvas.create_text((m1.x + m2.x) / 2,
        #                                 (m1.y + m2.y) / 2,
        #                                 text="COLLISION!",
        #                                 fill='red')
        #    self.canvas.after(1000, self.canvas.delete, text)
        #    m1.is_deleted = True
        #    m2.is_deleted = True
        if ( distance(m1, m2) < m1.radius + m2.radius ):
            logger.info("%s and %s collided!" % (m1.color, m2.color))
            self.canvas.delete(m1.canvas_id, m2.canvas_id)

            text = self.canvas.create_text((m1.x + m2.x) / 2,
                                         (m1.y + m2.y) / 2,
                                         text="COLLISION!",
                                         fill='red')
            self.canvas.after(1000, self.canvas.delete, text)

            #m1.is_deleted = True
            #m2.is_deleted = True
            print m1.x
            print m1.y
            print '*'*80
            for m in self.masses:
                print m.color
                print m.x
                print m.y
            self.masses.remove(m1)
            self.masses.remove(m2)
            mid_x = (m1.x + m2.x) / 2
            mid_y = (m1.y + m2.y) / 2
            c1 = m1.mass / (m1.mass + m2.mass)
            c2 = m2.mass / (m1.mass + m2.mass)
            v_x = c1 * m1.v_x + c2 * m2.v_x
            v_y = c1 * m1.v_y + c2 * m2.v_y

            A = avg_color(m1.color, m2.color)
            print 'A = ' + A

            new_m = MassiveObject(
                m1.mass + m2.mass,
                m1.radius + m2.radius,
                mid_x,
                mid_y,
                v_x,
                v_y,
                random_color()
                )
            new_m.canvas_id = self.canvas.create_oval(new_m.x - new_m.radius,
                                                   new_m.y - new_m.radius,
                                                   new_m.x + new_m.radius,
                                                   new_m.y + new_m.radius,
                                                   outline=new_m.color,
                                                   fill=new_m.color)
            self.masses.append(new_m)
            return

        old_x = m1.x
        old_y = m1.y
        g_x, g_y = grav_force(m1, m2)
        m1.a_x = g_x / m1.mass
        m1.a_y = g_y / m1.mass
        m1.t += m1.timestep
        m1.x += m1.timestep * (m1.v_x + .5*(m1.timestep * m1.a_x))
        m1.y += m1.timestep * (m1.v_y + .5*(m1.timestep * m1.a_y))
        g_x, g_y = grav_force(m1, m2)
        new_a_x, new_a_y = g_x / m1.mass, g_y / m1.mass
        m1.v_x += m1.timestep * .5 * (m1.a_x + new_a_x)
        m1.v_y += m1.timestep * .5 * (m1.a_y + new_a_y)

        self.canvas.move(m1.canvas_id, m1.x - old_x, m1.y - old_y)
        logger.info("Updated %s from (%s, %s) to (%s, %s)" % (m1.color, old_x, old_y, m1.x, m1.y))

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




if __name__ == '__main__':
    s = Simulator()

