class LegWithFoot:

    def __init__(self,
                 leg_length,
                 leg_color,
                 thickness_thigh=50,
                 thickness_foot=30,
                 foot_color="#ffff00"
                 ):
        self.leg_length = leg_length
        self.leg_color = leg_color
        self.thickness_foot = thickness_foot
        self.thickness_thigh = thickness_thigh
        self.foot_color = foot_color
    
    def render(self, dwg):
        g = dwg.g()

        leg = dwg.path(fill=self.leg_color)
        leg.push("M 0 0")
        leg.push("L 0 %f" % self.leg_length)
        leg.push("l %f 0" % self.thickness_foot)
        leg.push("L %f 0" % self.thickness_thigh)
        leg.push("Z")

        g.add(leg)

        boot_start = .7
        boot_height = 20
        foot_length = 50

        boot = dwg.path(fill=self.foot_color)
        boot.push("M 0 %f" % (self.leg_length * boot_start))
        boot.push("L 0 %f" % (self.leg_length + boot_height))
        boot.push("l %f 0" % foot_length)
        boot.push("a %f %f 0 0 0 %f %f" % (min(boot_height, abs(foot_length - self.thickness_foot)), boot_height, -min(boot_height, foot_length - self.thickness_foot), - boot_height))
        boot.push("L %f %f" % (self.thickness_thigh - (self.thickness_thigh - self.thickness_foot) * boot_start + 1, self.leg_length * boot_start))

        g.add(boot)

        return g