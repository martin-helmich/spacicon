from svgwrite import Drawing
import math

class PopEye:

    def __init__(self, radius, pupil_radius=.3, pupil_rho=0, pupil_phi=0):
        self.radius = radius
        self.pupil_radius = pupil_radius
        self.pupil_rho = pupil_rho
        self.pupil_phi = pupil_phi

    def render(self, dwg):
        g = dwg.g()

        eye = dwg.circle(center=(0, 0), r=self.radius, fill="white", stroke_width=0)
        g.add(eye)

        pupil_radius = self.radius * self.pupil_radius

        pupil_rho = min(
            self.radius * self.pupil_rho,
            self.radius * (1 - self.pupil_radius)
        )

        pupil_coords = (
            pupil_rho * math.cos(self.pupil_phi),
            pupil_rho * math.sin(self.pupil_phi)
        )

        pupil = dwg.circle(center=pupil_coords, r=pupil_radius, fill="black", stroke_width=0)
        g.add(pupil)

        reflection_radius = pupil_radius * .2
        reflection_rho = pupil_radius * .6
        reflection_phi = 1.75 * math.pi
        reflection_coords = (
            pupil_coords[0] + reflection_rho * math.cos(reflection_phi),
            pupil_coords[1] + reflection_rho * math.sin(reflection_phi)
        )

        reflection = dwg.circle(center=reflection_coords, r=reflection_radius, fill="white")

        g.add(reflection)

        return g