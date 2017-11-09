from flask import Flask
from objects.eye.pop import PopEye
from objects.arm.hand import ArmWithHand
from objects.leg.foot import LegWithFoot
from actors.alien.glorb import random_glorb
from actors.astronaut.dome import DomeHelmetAstronaut, random_domed_astronaut
from backgrounds.stars import StarsBackground
from svgwrite import Drawing
import math
import random

app = Flask(__name__)

@app.route("/objects/eye/pop")
def eye_pop():
    drawing = Drawing()

    e = PopEye(50, .6, .6, .5 * math.pi)
    g = e.render(drawing)
    g.translate(50, 50)

    drawing.add(g)

    return drawing.tostring()

@app.route("/objects/arms/hand")
def arm_hand():
    drawing = Drawing()

    r = drawing.rect((-50, -50), (200, 200), stroke="black", fill="white")
    drawing.add(r)

    a = ArmWithHand(arm_length=50, arm_color="#606060", hand_color="#ff0000")
    g = a.render(drawing)
    g.translate(50, 50)

    drawing.add(g)
    return drawing.tostring()

@app.route("/objects/legs/foot")
def leg_foot():
    drawing = Drawing()

    r = drawing.rect((-50, -50), (200, 200), stroke="black", fill="white")
    drawing.add(r)

    a = LegWithFoot(leg_length=50, leg_color="#606060", foot_color="#ff0000")
    g = a.render(drawing)
    g.translate(50, 50)

    drawing.add(g)
    return drawing.tostring()

@app.route("/actors/alien/glorb")
def alien_glorb():
    drawing = Drawing()
    prng = random.Random()

    #background = drawing.rect((0,0), size=(200,200), fill="black")
    background = StarsBackground(200, 200)
    drawing.add(background.render(drawing))

    #a = GlorbAlien(position=(75, 75), size=60)
    a = random_glorb(prng, size=prng.randint(40, 80))
    g = a.render(drawing)
    g.translate(prng.randint(50, 150), prng.randint(50, 150))
    g.rotate(prng.gauss(0, 20))

    drawing.add(g)

    return drawing.tostring()

@app.route("/actors/astronaut/glorb")
def astro_glorb():
    drawing = Drawing()
    prng = random.Random()

    #background = drawing.rect((0,0), size=(200,200), fill="black")
    background = StarsBackground(300, 300)
    drawing.add(background.render(drawing))

    #a = GlorbAlien(position=(75, 75), size=60)
    a = random_glorb(prng, size=prng.randint(40, 80))
    #astro = DomeHelmetAstronaut(a, a.size)
    astro = random_domed_astronaut(prng, a)
    g = astro.render(drawing)
    g.translate(prng.randint(100, 200), prng.randint(100, 200))
    g.rotate(prng.gauss(0, 20))

    drawing.add(g)

    return drawing.tostring()
