from math import sqrt


def distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def grav_force(p1, p2):
    d = distance(p1.x, p1.y, p2.x, p2.y)
    G = 6.67 * 10 ** -11
    f = (G * p1.mass * p2.mass) / (d ** 2)
    return f * (p2.x - p1.x) / d, f * (p2.y - p1.y) / d


def elastic_headon_collision(m1, v1, m2, v2):
    m1_plus_m2 = m1 + m2
    v2_final = (2 * m1 * v1 / m1_plus_m2) - ((m1 - m2) * v2 / m1_plus_m2)
    v1_final = ((m1 - m2) * v1 / m1_plus_m2) + (2 * m2 * v2 / m1_plus_m2)
    return v1_final, v2_final
