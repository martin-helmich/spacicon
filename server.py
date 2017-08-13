from flask import Flask
from objects.eye.pop import PopEye
from actors.alien.glorb import GlorbAlien, random_glorb
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