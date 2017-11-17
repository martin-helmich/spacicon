from svgwrite import Drawing
from svgwrite.container import Group

class Renderable:

    def render(self, dwg: Drawing) -> Group:
        pass