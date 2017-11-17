from random import Random

def darken_hex(color: str, amount: float = .1) -> str:
    if color[0] == "#":
        color = color[1:]
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    r = min(255, max(0, round(r * (1 - amount))))
    g = min(255, max(0, round(g * (1 - amount))))
    b = min(255, max(0, round(b * (1 - amount))))

    return "#%02x%02x%02x" % (r, g, b)

def lighten_hex(color: str, amount: float = .1) -> str:
    return darken_hex(color, -amount)

def random_hex(prng: Random) -> str:
    return "#%02x%02x%02x" % (prng.randint(0, 255), prng.randint(0, 255), prng.randint(0, 255))