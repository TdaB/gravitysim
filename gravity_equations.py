from math import sqrt


def mag(x1, y1, x2, y2):
    return sqrt( (x2 - x1)**2 + (y2 - y1)**2 )

def distance(p1, p2):
    return sqrt( (p2.x - p1.x)**2 + (p2.y - p1.y)**2 )

def grav_force(p1, p2):
    d = distance(p1, p2)
    G = 6.67 * 10**-11
    f = (G * p1.mass * p2.mass) / (d**2)
    return f * (p2.x - p1.x) / d, f * (p2.y - p1.y) / d
