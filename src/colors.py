from random import choice


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
    rgb_hex = [hex(r)[2:], hex(g)[2:], hex(b)[2:]]
    for i, h in enumerate(rgb_hex):
        if len(h) == 1:
            rgb_hex[i] = '0' + h
    result = '#' + rgb_hex[0] + rgb_hex[1] + rgb_hex[2] 
    return result
