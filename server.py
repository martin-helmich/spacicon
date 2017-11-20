from flask import Flask, request, Response, send_file
from flask_caching import Cache
from objects import Renderable
from objects.eye.pop import PopEye
from objects.arm.hand import ArmWithHand
from objects.leg.foot import LegWithFoot
from actors.alien.glorb import random_glorb
from actors.astronaut.dome import DomeHelmetAstronaut, random_domed_astronaut
from backgrounds.stars import StarsBackground
from backgrounds.nasaimg import random_background
from backgrounds.linked import LinkedBackground
from svgwrite import Drawing
from cairosvg import svg2png
from typing import Tuple, Any, Union
from random import Random
import math
import random
import os

app = Flask(__name__)

cache_config = {key: val for key, val in os.environ.items() if key.startswith("CACHE_")}
print("Using cache config %s", cache_config)
cache = Cache(app, config=cache_config)

@app.route("/objects/eye/pop")
def eye_pop() -> str:
    drawing = Drawing()

    e = PopEye(50, .6, .6, .5 * math.pi)
    g = e.render(drawing)
    g.translate(50, 50)

    drawing.add(g)

    return drawing.tostring()

@app.route("/objects/arms/hand")
def arm_hand() -> str:
    drawing = Drawing()

    r = drawing.rect((-50, -50), (200, 200), stroke="black", fill="white")
    drawing.add(r)

    a = ArmWithHand(arm_length=50, arm_color="#606060", hand_color="#ff0000")
    g = a.render(drawing)
    g.translate(50, 50)

    drawing.add(g)
    return drawing.tostring()

@app.route("/objects/legs/foot")
def leg_foot() -> str:
    drawing = Drawing()

    r = drawing.rect((-50, -50), (200, 200), stroke="black", fill="white")
    drawing.add(r)

    a = LegWithFoot(leg_length=50, leg_color="#606060", foot_color="#ff0000")
    g = a.render(drawing)
    g.translate(50, 50)

    drawing.add(g)
    return drawing.tostring()

@app.route("/actors/alien/glorb")
def alien_glorb() -> str:
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
def astro_glorb() -> str:
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

@app.route("/assets/<file>")
def serve_asset(file: str) -> Response:
    return send_file("assets/backgrounds/%s" % file, mimetype="image/jpeg")

@app.route("/team/<id>/background")
@cache.cached(timeout=86400 * 30, query_string=True)
def team_background(id: str) -> Response:
    drawing = Drawing()
    team_prng = Random(id)

    width = request.args.get("w", default=1000)
    height = request.args.get("h", default=400)

    drawing["width"] = "%dpx" % width
    drawing["height"] = "%dpx" % height

    background = random_background(team_prng, width, height, local_paths=True)
    drawing.add(background.render(drawing))

    svg_code = drawing.tostring()

    res = Response(svg2png(bytestring=bytearray(svg_code, "utf-8"), scale=1))
    res.headers["Content-Type"] = "image/png"
    return res

@app.route("/team/<id>.<format>")
@cache.cached(timeout=86400, query_string=True)
def team(id: str, format: str) -> Union[Response, Tuple[Any, int]]:
    drawing = Drawing()

    w = 1000
    h = 400

    drawing["width"] = "%dpx" % w
    drawing["height"] = "%dpx" % h

    team_id = id
    emails = request.args.getlist("emails")[0:10]
    generate_random = request.args.get("random")

    if generate_random:
        team_id = random.random()
        email_count = random.randint(1, 8)
        emails = [random.random() for r in range(email_count)]

    team_prng = Random(team_id)

    background: Renderable
    if format == "png":
        background = random_background(team_prng, w, h, local_paths=format == "png")
    else:
        host = request.host
        url = "//%s/team/%s/background" % (host, team_id)
        background = LinkedBackground(url, w, h)

    drawing.add(background.render(drawing))

    distance = w / (len(emails) + 1)

    max_size = 80 - (len(emails) - 4) * 7

    for i, email in enumerate(emails):
        prng = random.Random(email)

        a = random_glorb(prng, size=prng.randint(math.floor(max_size * .5), math.floor(max_size * .7)))
        
        astro = random_domed_astronaut(prng, a)
        
        g = astro.render(drawing)
        g.translate((i + 1) * distance , team_prng.randint(100, 200))
        g.rotate(team_prng.gauss(0, 20))

        drawing.add(g)
    
    svg_code = drawing.tostring()

    if format == "svg":
        res = Response(drawing.tostring())
        res.headers["Content-Type"] = "image/svg+xml"
        return res
    elif format == "png":
        requested_width: int
        try:
            requested_width = int(request.args.get("s"))
        except:
            requested_width = 1000

        res = Response(svg2png(bytestring=bytearray(svg_code, "utf-8"), scale=requested_width/w))
        res.headers["Content-Type"] = "image/png"
        return res

    return None, 406