import helper.colors
from objects import Renderable
from random import Random
from svgwrite import Drawing
from svgwrite.container import Group

class StarsBackground(Renderable):

    def __init__(self,
                 w: int, 
                 h: int, 
                 color: str = helper.colors.darken_hex("#0000ff", 0.8), 
                 prng: Random = Random()) -> None:
        self.width = w
        self.height = h
        self.color = color
        self.prng = prng
    
    def render(self, dwg: Drawing) -> Group:
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