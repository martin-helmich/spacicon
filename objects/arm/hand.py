from math import pi, sin, cos
import helper.colors

class ArmWithHand:

    def __init__(self,
                 arm_length,
                 arm_color,
                 thickness_shoulder=30,
                 thickness_hand=None,
                 hand_finger_count=4,
                 hand_finger_length=None,
                 hand_finger_spread=.3 * pi,
                 hand_color="#ffff00",
                 reverse_shadow=False):
        if thickness_hand is None:
            thickness_hand = thickness_shoulder / 3 * 2
        if hand_finger_length is None:
            hand_finger_length = thickness_hand

        self.arm_length = arm_length
        self.arm_color = arm_color
        self.thickness_hand = thickness_hand
        self.thickness_shoulder = thickness_shoulder
        self.hand_finger_count = hand_finger_count
        self.hand_finger_spread = hand_finger_spread
        self.hand_finger_length = hand_finger_length
        self.hand_color = hand_color
        self.reverse_shadow = reverse_shadow

    def render(self, dwg):
        g = dwg.g()

        arm = dwg.path(fill=self.arm_color)
        arm.push("M 0 %f" % (-self.thickness_shoulder / 2))
        arm.push("L %f %f" % (self.arm_length, -self.thickness_hand / 2))
        arm.push("l 0 %f" % self.thickness_hand)
        arm.push("L %f %f" % (-20, self.thickness_shoulder / 2))
        arm.push("Z")

        finger_phi = self.hand_finger_spread / (self.hand_finger_count)
        finger_phi_first = - self.hand_finger_spread / 2

        finger_thinkness = self.thickness_hand / self.hand_finger_count
        finger_base_range = self.thickness_hand - finger_thinkness / 2
        finger_base_delta = finger_base_range / self.hand_finger_count
        finger_first_y = -(self.thickness_shoulder - self.thickness_hand) / 2 

        for i in range(self.hand_finger_count):
            phi = finger_phi_first + (i) * finger_phi
            length = self.hand_finger_length
            thickness = self.thickness_hand / self.hand_finger_count

            if i == 0:
                length *= .8

            if i == self.hand_finger_count - 1:
                length *= .7
                thickness *= 1.1
                phi += finger_phi

            finger = dwg.path(stroke_width=thickness, stroke=self.hand_color, stroke_linecap="round")
            finger.push("M %f %f" % (self.arm_length, finger_first_y + i * finger_base_delta))
            finger.push("l %f %f" % (length * cos(phi), length * sin(phi)))

            g.add(finger)
        
        g.add(arm)

        shadow_color = helper.colors.darken_hex(self.arm_color, .2)
        shadow = dwg.path(fill=shadow_color)

        shadow.push("M %f %f" % (-20, self.thickness_shoulder / 2))
        shadow.push("L %f %f" % (self.arm_length, self.thickness_hand / 2))
        shadow.push("l 0 %f" % -(self.thickness_hand * .2))
        shadow.push("L -20 %f" % (self.thickness_shoulder / 2 * .2))
        shadow.push("Z")

        g.add(shadow)

        glove_start = .7
        glove = dwg.path(fill=self.hand_color)
        glove.push("M %f %f" % (self.arm_length * glove_start, (-self.thickness_shoulder / 2) + (self.thickness_shoulder - self.thickness_hand) / 2 * glove_start - 1))
        glove.push("L %f %f" % (self.arm_length, -self.thickness_hand / 2))
        glove.push("l %f 0" % (self.hand_finger_length * .4))
        glove.push("l 0 %f" % self.thickness_hand)
        glove.push("l %f 0" % (-self.hand_finger_length * .4))
        glove.push("L %f %f" % (self.arm_length * glove_start, (self.thickness_shoulder / 2) - (self.thickness_shoulder - self.thickness_hand) / 2 * glove_start + 1))

        g.add(glove)

        return g


