class PlainHappyMouth:

    def __init__(self, width, color, intensity=.2):
        self.width = width
        self.color = color
        self.intensity = intensity
    
    def render(self, dwg):
        g = dwg.g()

        p = dwg.path(stroke=self.color, fill_opacity=0, stroke_width=3)
        p.push("M %f %f" % (-self.width / 2, 0))
        p.push("Q %f %f %f %f" % (0, self.width * self.intensity, self.width / 2, 0))
        #p.push("Z")

        g.add(p)

        return g

class PlainGrumpyMouth(PlainHappyMouth):

    def __init__(self, width, color, intensity=.2):
        PlainHappyMouth.__init__(self, width=width, color=color, intensity=-intensity)

class PlainLaughingMouth:

    def __init__(self, width, color, intensity=.2):
        self.width = width
        self.color = color
        self.intensity = intensity
    
    def render(self, dwg):
        g = dwg.g()

        p = dwg.path(fill="black", stroke_width=0)
        p.push("M %f %f" % (-self.width / 2, 0))
        p.push("Q %f %f %f %f" % (0, self.width * self.intensity, self.width / 2, 0))
        p.push("Z")

        g.add(p)

        return g