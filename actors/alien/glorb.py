from objects.eye.pop import PopEye
from objects.mouth.plain import PlainHappyMouth, PlainLaughingMouth, PlainGrumpyMouth
import math
import uuid
import helper.colors
import helper.random
import random

squint_chance = .1
differently_dilated_chance = .05

def random_glorb(prng, size):
    """
    Generates a random Glorb.

    :param prng random.Random: An instance of a PRNG
    """

    squinting = prng.random() <= squint_chance
    differently_dilated = prng.random() <= differently_dilated_chance

    if not squinting:
        pupil_phi_static = prng.uniform(0, 2 * math.pi)
        pupil_phi = lambda: pupil_phi_static

        pupil_rho_static = prng.expovariate(5)
        pupil_rho = lambda: pupil_rho_static
    else:
        pupil_phi = lambda: prng.uniform(0, 2 * math.pi)
        pupil_rho = lambda: prng.expovariate(5)
    
    if not differently_dilated:
        pupil_radius_static = prng.uniform(.2, .8)
        pupil_radius = lambda: pupil_radius_static
    else:
        pupil_radius = lambda: prng.uniform(.2, .8)
    
    mouths = [
        PlainHappyMouth,
        PlainLaughingMouth,
        PlainGrumpyMouth
    ]

    def pop_eye_factory(size):
        return PopEye(radius=size,
                      pupil_radius=pupil_radius(),
                      pupil_rho=pupil_rho(),
                      pupil_phi=pupil_phi())
    
    def plain_mouth_factory(width, color):
        mouth = prng.choice(mouths)
        return mouth(width=width, color=color, intensity=prng.gauss(.3, .1))

    eye_count = prng.randint(1,2) * 2 - 1

    return GlorbAlien(size=size,
                      eye_count=eye_count,
                      eye_factory=pop_eye_factory,
                      eye_relative_size=prng.random() * .15 + .2,
                      eye_distance=prng.random() * .2 + 0.65,
                      mouth_factory=plain_mouth_factory,
                      mouth_relative_size=prng.gauss(1, .3),
                      mouth_height=prng.uniform(.3, .7),
                      antennae_count=prng.randint(1, 3),
                      antennae_relative_size=helper.random.gauss_limited(prng, .2, .1, .1, .3),
                      color=helper.colors.random_hex(prng))

class GlorbAlien:

    def __init__(self,
                 size,

                 eye_count=3, 
                 eye_factory=PopEye,
                 eye_relative_size=.3, 
                 eye_distance=.75,

                 mouth_factory=PlainHappyMouth,
                 mouth_relative_size=1.2,
                 mouth_height=.5,

                 antennae_count=2,
                 antennae_rho=1.3,
                 antennae_relative_size=.2,

                 color="#ffaa00"):
        self.id = uuid.uuid4()
        self.size = size
        self.color = color

        self.eye_count = eye_count
        self.eye_factory = eye_factory
        self.eye_relative_size = eye_relative_size
        self.eye_distance = eye_distance

        self.mouth_factory = mouth_factory
        self.mouth_relative_size = mouth_relative_size
        self.mouth_height = mouth_height

        self.antennae_count = antennae_count
        self.antennae_relative_size = antennae_relative_size
        self.antennae_rho = max(antennae_rho, antennae_relative_size + 1.1)

    def render(self, dwg):
        g = dwg.g()

        # Render antennae
        antennae_rho = self.size * self.antennae_rho
        antennae_base_phi = 1.5 * math.pi
        antennae_delta_phi = 0.4 * math.pi
        antennae_delta_phi_total = (self.antennae_count - 1) * antennae_delta_phi
        antennae_left_phi = antennae_base_phi - antennae_delta_phi_total / 2
        antennae = []

        for i in range(self.antennae_count):
            antennae_coords = (
                antennae_rho * math.cos(antennae_left_phi + i * antennae_delta_phi),
                antennae_rho * math.sin(antennae_left_phi + i * antennae_delta_phi)
            )

            antenna = dwg.circle(center=antennae_coords, r=self.size * self.antennae_relative_size, fill=self.color)

            path = dwg.path(stroke=helper.colors.darken_hex(self.color), stroke_width=3)
            path.push("M %f %f" % antennae_coords)
            path.push("L %f %f" % (0, 0))

            g.add(path)
            g.add(antenna)

        # Render body
        shadow_mask = dwg.defs.add(dwg.clipPath(id="bodymask-%s" % self.id))
        shadow_mask.add(dwg.circle(center=(0, 0), r=self.size))

        body_dark = dwg.circle(center=(0, 0), 
                               r=self.size, 
                               stroke_width=0, 
                               fill=helper.colors.darken_hex(self.color),
                               clip_path="url(#bodymask-%s)" % self.id)
        g.add(body_dark)

        body_highlight = dwg.circle(center=(- self.size * .2, - self.size * .2), 
                                    r=self.size * .95, 
                                    stroke_width=0, 
                                    fill=self.color,
                                    clip_path="url(#bodymask-%s)" % self.id)
        g.add(body_highlight)


        # Render eyes
        eye_rho = self.size * self.eye_distance
        eye_base_phi = 1.5 * math.pi
        eye_delta_phi = 0.3 * math.pi
        eye_delta_phi_total = (self.eye_count - 1) * eye_delta_phi
        eye_left_phi = eye_base_phi - eye_delta_phi_total / 2
        eyes = []

        for eye_i in range(self.eye_count):
            eye_coords = (
                eye_rho * math.cos(eye_left_phi + eye_i * eye_delta_phi),
                eye_rho * math.sin(eye_left_phi + eye_i * eye_delta_phi)
            )

            eye = self.eye_factory(self.size * self.eye_relative_size)
            eye_g = eye.render(dwg)
            eye_g.translate(eye_coords[0], eye_coords[1])

            g.add(eye_g)

        # Render mouth
        mouth = self.mouth_factory(self.size * self.mouth_relative_size, helper.colors.darken_hex(self.color, .75))
        mouth_g = mouth.render(dwg)
        mouth_g.translate(0, self.size * self.mouth_height)

        g.add(mouth_g)

        return g
