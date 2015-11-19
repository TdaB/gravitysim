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
            self.masses.append( MassiveObject(
                self.canvas,
                size * 10**16,
                size,
                randint(10, self.width - 10),
                randint(10, self.height - 10),
                randint(-15, 15),
                randint(-15, 15),
                self.random_color()
                )
            )
        self.canvas.pack()

        self.draw()
        tk.mainloop()

    def random_color(self):
        choices = [str(n) for n in range(9)] + [c for c in 'abcdef']
        result = '#'
        for _ in range(6):
            result += choice(choices)
        return result

    def draw(self):
        for m in self.masses:
            if m.is_deleted is True:
                self.masses.remove(m)
                continue
            for m2 in self.masses:
                if m2 == m:
                    continue
                else:
                    m.update(m2)
            m.draw_accel_vector()
            m.draw_vel_vector()
        self.canvas.after(10, self.draw)


if __name__ == '__main__':
    s = Simulator()
