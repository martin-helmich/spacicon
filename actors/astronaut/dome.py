import helper.colors
import helper.random
import uuid
import math
from objects.arm.hand import ArmWithHand
from objects.leg.foot import LegWithFoot
from objects import Renderable
from random import Random
from typing import List, Tuple
from svgwrite import Drawing
from svgwrite.container import Group

SOCKET_COLORS: List[str] = [
    "#606060",
    "#D49090",
    "#6D9C68"
]

BODY_COLORS: List[str] = [
    "#303030",
    helper.colors.darken_hex("#D49090", .5),
    helper.colors.darken_hex("#6D9C68", .5)
]

class DomeHelmetAstronaut:

    def __init__(self,
                 head: Renderable,
                 head_size: int,
                 socket_color: str = "#606060",
                 body_color: str = "#303030",
                 body_fatness: float = .8,
                 body_height: float = 2,
                 body_left_arm_angle: float = .3 * math.pi,
                 body_right_arm_angle: float = .2 * math.pi,
                 legs_height: float = 1.5,
                 arm_count: int = 2,
                 arm_params={},
                 leg_params={},
                 ) -> None:
        self.id = uuid.uuid4()
        self.head = head
        self.head_size = head_size
        self.socket_color = socket_color

        self.body_color = body_color
        self.body_fatness = body_fatness
        self.body_height = body_height
        self.body_left_arm_angle = body_left_arm_angle
        self.body_right_arm_angle = body_right_arm_angle

        self.arm_params = arm_params
        self.arm_count = arm_count

        self.leg_params = leg_params
        self.legs_height = legs_height

    def render(self, dwg: Drawing) -> Group:
        g = dwg.g()

        head = self.head.render(dwg)

        socket_relative_width = 1.2

        socket_radius = (self.head_size * socket_relative_width, self.head_size*0.3)
        socket_relative_height = .3

        socket_left = (-self.head_size * socket_relative_width, self.head_size * .5)
        socket_left_bottom = (socket_left[0], socket_left[1] + self.head_size * socket_relative_height)
        socket_right: Tuple[float, float] = (self.head_size * socket_relative_width, self.head_size * .5)
        socket_right_bottom: Tuple[float, float] = (socket_right[0], socket_right[1] + self.head_size * socket_relative_height)

        size_factor = self.head_size / 50.0

        arm_length = 50 * size_factor
        arm_params = {
            "arm_length": arm_length,
            "arm_color": self.body_color,
            "hand_color": helper.colors.lighten_hex(self.body_color, 2),
            "thickness_shoulder": 30 * size_factor
        }
        arm_params.update(self.arm_params)

        for i in range(self.arm_count):
            left_arm = ArmWithHand(**arm_params) # type: ignore
            left_arm_g = left_arm.render(dwg)

            left_arm_x = socket_right_bottom[0] - left_arm.thickness_shoulder / 2 - (socket_right_bottom[0] - self.head_size * self.body_fatness) / (self.head_size * self.body_height) * i * left_arm.thickness_shoulder * 1.2

            left_arm_g.translate(left_arm_x, socket_right_bottom[1] + left_arm.thickness_shoulder / 2 + i * left_arm.thickness_shoulder * .8)
            left_arm_g.rotate(self.body_left_arm_angle / (math.pi) * 180 + (i * 20))

            g.add(left_arm_g)

            right_arm = ArmWithHand(reverse_shadow=True, **arm_params) # type: ignore
            right_arm_g = right_arm.render(dwg)

            right_arm_x = socket_left_bottom[0] + right_arm.thickness_shoulder / 2 + (-self.head_size * self.body_fatness - socket_left_bottom[0]) / (self.head_size * self.body_height) * i * right_arm.thickness_shoulder * 1.2

            right_arm_g.translate(right_arm_x, socket_left_bottom[1] + right_arm.thickness_shoulder / 2 + i * right_arm.thickness_shoulder * .8)
            right_arm_g.rotate(-self.body_right_arm_angle / (math.pi) * 180 - (i * 20))
            right_arm_g.scale(-1, 1)

            g.add(right_arm_g)

        leg_thickness_thigh = self.body_fatness * self.head_size
        leg_thickness_foot = leg_thickness_thigh * .7

        leg_length = self.head_size * 1

        boot_height = leg_length * .5
        foot_length = leg_length

        left_leg = LegWithFoot(leg_length=leg_length, # type: ignore
                               leg_color=self.body_color,
                               thickness_thigh=leg_thickness_thigh,
                               thickness_foot=leg_thickness_foot,
                               foot_color=helper.colors.lighten_hex(self.body_color, 2),
                               boot_height=boot_height,
                               foot_length=foot_length,
                               **self.leg_params)
        left_leg_g = left_leg.render(dwg)
        left_leg_g.translate(0, self.head_size * self.body_height)
        left_leg_g.rotate(-20)

        g.add(left_leg_g)

        right_leg = LegWithFoot(leg_length=leg_length, # type: ignore
                                leg_color=self.body_color,
                                thickness_thigh=leg_thickness_thigh,
                                thickness_foot=leg_thickness_foot,
                                foot_color=helper.colors.lighten_hex(self.body_color, 2),
                                boot_height=boot_height,
                                foot_length=foot_length,
                                **self.leg_params)
        right_leg_g = right_leg.render(dwg)
        right_leg_g.translate(0, self.head_size * self.body_height)
        right_leg_g.rotate(20)
        right_leg_g.scale(-1, 1)

        g.add(right_leg_g)

        body = dwg.path(fill=self.body_color)
        body.push("M %f %f" % (socket_right_bottom[0], socket_right_bottom[1]))
        body.push("L %f %f" % (self.head_size * self.body_fatness, self.head_size * self.body_height))
        body.push("L %f %f" % (self.head_size * (self.body_fatness - .2), self.head_size * (self.body_height + .2)))
        body.push("L %f %f" % (-self.head_size * (self.body_fatness - .2), self.head_size * (self.body_height + .2)))
        body.push("L %f %f" % (-self.head_size * self.body_fatness, self.head_size * self.body_height))
        body.push("L %f %f" % (socket_left_bottom[0], socket_left_bottom[1]))

        g.add(body)

        socket_background_color = helper.colors.darken_hex(self.socket_color)
        socket_background = dwg.ellipse(fill=socket_background_color, center=(0, self.head_size * .5), r=socket_radius)
        
        socket_foreground = dwg.path(fill=self.socket_color)
        socket_foreground.push("M %f %f" % socket_left)
        socket_foreground.push("A %f %f 0 0 0 %f %f" % (socket_radius[0], socket_radius[1], socket_right[0], socket_right[1]))
        socket_foreground.push("l 0 %f" % (self.head_size * .3))
        socket_foreground.push("A %f %f 0 0 1 %f %f" % (socket_radius[0], socket_radius[1], - self.head_size * socket_relative_width, self.head_size * .8))

        g.add(socket_background)
        g.add(head)
        g.add(socket_foreground)

        dome = dwg.path(fill="white", fill_opacity=.3)
        dome.push("M %f %f" % socket_left)
        dome.push("C %f %f %f %f %f %f" % (-self.head_size * (socket_relative_width + 1),
                                           -self.head_size * 3,
                                           self.head_size * (socket_relative_width + 1),
                                           -self.head_size * 3,
                                           socket_right[0],
                                           socket_right[1]))
        dome.push("A %f %f 0 0 1 %f %f" % (socket_radius[0], socket_radius[1], socket_left[0], socket_left[1]))

        refl_mask = dwg.defs.add(dwg.mask((self.head_size * -1.5, self.head_size * -2.5),
                                          (self.head_size * 3, self.head_size * 5),
                                          id="%s-dome-refl-mask" % self.id))
        refl_mask.add(dwg.rect((self.head_size * -1.5, self.head_size * -2.5),
                                          (self.head_size * 3, self.head_size * 5), fill="white"))
        refl_mask.add(dwg.circle((self.head_size * .3, -self.head_size * .25), r=self.head_size * 1.75, fill="black"))

        dome_reflection = dwg.path(fill="white", fill_opacity=.3, mask="url(#%s-dome-refl-mask)" % self.id)
        dome_reflection.push("M %f %f" % socket_left)
        dome_reflection.push("C %f %f %f %f %f %f" % (-self.head_size * (socket_relative_width + 1),
                                           -self.head_size * 3,
                                           self.head_size * (socket_relative_width + 1),
                                           -self.head_size * 3,
                                           socket_right[0],
                                           socket_right[1]))
        dome_reflection.push("A %f %f 0 0 1 %f %f" % (socket_radius[0], socket_radius[1], socket_left[0], socket_left[1]))
        dome_reflection.scale(.9)

        g.add(dome)
        g.add(dome_reflection)

        return g

def random_domed_astronaut(prng: Random, head) -> DomeHelmetAstronaut:
    return DomeHelmetAstronaut(head,
                               head.size,
                               socket_color=prng.choice(SOCKET_COLORS),
                               body_color=prng.choice(BODY_COLORS),
                               body_fatness=helper.random.gauss_limited(prng, .8, .1),
                               body_height=helper.random.gauss_limited(prng, 2., .25),
                               body_left_arm_angle=prng.uniform(-.3, .3) * math.pi,
                               body_right_arm_angle=prng.uniform(-.3, .3) * math.pi,
                               legs_height=helper.random.gauss_limited(prng, 1.5, .25),
                               arm_count=prng.randint(1, 2)
                               )
