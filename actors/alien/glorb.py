from objects.eye.pop import PopEye
import math
import uuid
import helper.colors
import random

squint_chance = .1
differently_dilated_chance = .05

def random_glorb(prng, position, size):
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

    def pop_eye_factory(position, size):
        return PopEye(position=position,
                      radius=size,
                      pupil_radius=pupil_radius(),
                      pupil_rho=pupil_rho(),
                      pupil_phi=pupil_phi())

    return GlorbAlien(position=position,
                      size=size,
                      eye_count=prng.randint(1, 3),
                      eye_factory=pop_eye_factory,
                      eye_relative_size=prng.random() * .15 + .2,
                      eye_distance=prng.random() * .2 + 0.65,
                      color=helper.colors.random_hex(prng))

class GlorbAlien:

    def __init__(self,
                 position, 
                 size, 
                 eye_count=3, 
                 eye_factory=PopEye,
                 eye_relative_size=.3, 
                 eye_distance=.75,
                 color="#ffaa00"):
        self.id = uuid.uuid4()
        self.position = position
        self.size = size
        self.color = color
        self.eye_count = eye_count
        self.eye_factory = eye_factory
        self.eye_relative_size = eye_relative_size
        self.eye_distance = eye_distance

    def render(self, dwg):
        # Render body
        g = dwg.g()
        shadow_mask = dwg.defs.add(dwg.clipPath(id="bodymask-%s" % self.id))
        shadow_mask.add(dwg.circle(center=self.position, r=self.size))

        body_dark = dwg.circle(center=self.position, 
                               r=self.size, 
                               stroke_width=0, 
                               fill=helper.colors.darken_hex(self.color),
                               clip_path="url(#bodymask-%s)" % self.id)
        g.add(body_dark)

        body_highlight = dwg.circle(center=(self.position[0] - self.size * .2, self.position[1] - self.size * .2), 
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
                self.position[0] + eye_rho * math.cos(eye_left_phi + eye_i * eye_delta_phi),
                self.position[1] + eye_rho * math.sin(eye_left_phi + eye_i * eye_delta_phi)
            )

            eye = self.eye_factory(eye_coords, self.size * self.eye_relative_size)
            eye_g = eye.render(dwg)

            g.add(eye_g)

        return g
