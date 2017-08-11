import helper.colors
import random

class StarsBackground:

    def __init__(self, w, h, color = helper.colors.darken_hex("#0000ff", 0.8), prng = random.Random()):
        self.width = w
        self.height = h
        self.color = color
        self.prng = prng
    
    def render(self, dwg):
        r = dwg.rect(insert=(0, 0),
                     size=(self.width, self.height),
                     fill=self.color)
        g = dwg.g()
        g.add(r)

        star_count = int(self.width * self.height * .001)
        for i in range(star_count):
            s = dwg.circle(center=(self.prng.randint(0, self.width), self.prng.randint(0, self.height)),
                           r=max(2, self.prng.gauss(1, 1)),
                           fill="white")
            g.add(s)

        return g