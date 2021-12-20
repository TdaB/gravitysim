import configparser
from math import sqrt

config = configparser.ConfigParser()
config.read('../config.ini')
meters_per_pixel = config.getint('DEFAULT', 'meters.per.pixel')


def distance(x1, y1, x2, y2):
    return sqrt(((x2 - x1) * meters_per_pixel) ** 2 + ((y2 - y1) * meters_per_pixel) ** 2)


def grav_force(m1, m2):
    """
    Calculates the gravitational force on m1 by m2.
    @param m1: Massive object 1
    @param m2: Massive object 2
    @return: Force x component, force y component
    """
    d = distance(m1.x, m1.y, m2.x, m2.y)
    G = 6.67 * 10 ** -11
    f = (G * m1.mass * m2.mass) / (d ** 2)
    return f * (m2.x - m1.x) * meters_per_pixel / d, f * (m2.y - m1.y) * meters_per_pixel / d


def elastic_headon_collision(m1, v1, m2, v2):
    m1_plus_m2 = m1 + m2
    v2_final = (2 * m1 * v1 / m1_plus_m2) - ((m1 - m2) * v2 / m1_plus_m2)
    v1_final = ((m1 - m2) * v1 / m1_plus_m2) + (2 * m2 * v2 / m1_plus_m2)
    return v1_final, v2_final
