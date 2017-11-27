from objects import Renderable
from svgwrite import Drawing
from svgwrite.container import Group
import base64

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

class EmbeddedBackground(Renderable):

    def __init__(self, data: bytearray, width: int, height: int) -> None:
        self.data = data
        self.width = width
        self.height = height

    def render(self, d: Drawing) -> Group:
        g = d.g()
        href = "data:image/jpeg;base64,%s" % base64.b64encode(self.data).decode()

        r = d.image(href=href)
        r["xlink:href"] = href
        r["width"] = "%dpx" % self.width
        r["height"] = "%dpx" % self.height

        g.add(r)
        return g
