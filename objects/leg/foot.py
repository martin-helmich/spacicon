from svgwrite import Drawing
from svgwrite.container import Group

class LegWithFoot:

    def __init__(self,
                 leg_length: float,
                 leg_color: str,
                 thickness_thigh: float = 50,
                 thickness_foot: float = 30,
                 boot_height: float = 20,
                 foot_length: float = 50,
                 foot_color: str = "#ffff00"
                 ) -> None:
        self.leg_length = leg_length
        self.leg_color = leg_color
        self.thickness_foot = thickness_foot
        self.thickness_thigh = thickness_thigh
        self.foot_color = foot_color
        self.boot_height = boot_height
        self.foot_length = foot_length
    
    def render(self, dwg: Drawing) -> Group:
        g = dwg.g()

        leg = dwg.path(fill=self.leg_color)
        leg.push("M 0 0")
        leg.push("L 0 %f" % self.leg_length)
        leg.push("l %f 0" % self.thickness_foot)
        leg.push("L %f 0" % self.thickness_thigh)
        leg.push("Z")

        g.add(leg)

        boot_start = .7
        boot_height = self.boot_height
        foot_length = self.foot_length

        boot = dwg.path(fill=self.foot_color)
        boot.push("M 0 %f" % (self.leg_length * boot_start))
        boot.push("L 0 %f" % (self.leg_length + boot_height))
        boot.push("l %f 0" % foot_length)
        boot.push("a %f %f 0 0 0 %f %f" % (min(boot_height, abs(foot_length - self.thickness_foot)), boot_height, -min(boot_height, foot_length - self.thickness_foot), - boot_height))
        boot.push("L %f %f" % (self.thickness_thigh - (self.thickness_thigh - self.thickness_foot) * boot_start + 1, self.leg_length * boot_start))

        g.add(boot)

        return g