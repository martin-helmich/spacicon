def darken_hex(color, amount=.1):
    if color[0] == "#":
        color = color[1:]
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    r = max(0, r * (1 - amount))
    g = max(0, g * (1 - amount))
    b = max(0, b * (1 - amount))

    return "#%02x%02x%02x" % (r, g, b)

def random_hex(prng):
    return "#%02x%02x%02x" % (prng.randint(0, 255), prng.randint(0, 255), prng.randint(0, 255))