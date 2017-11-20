from objects import Renderable
from svgwrite import Drawing
from svgwrite.container import Group

class LinkedBackground(Renderable):
    
    def __init__(self, href: str, width: int, height: int) -> None:
        self.href = href
        self.width = width
        self.height = height
    
    def render(self, d: Drawing) -> Group:
        g = d.g()

        r = d.image(href=self.href)
        r["xlink:href"] = self.href
        r["width"] = "%dpx" % self.width
        r["height"] = "%dpx" % self.height

        g.add(r)
        return g