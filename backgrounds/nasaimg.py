import helper.colors
import os
import os.path
from objects import Renderable
from random import Random
from svgwrite import Drawing
from svgwrite.container import Group
from PIL import Image

ASSET_DIR = os.path.realpath(os.path.dirname(__file__) + "/../assets/backgrounds")

class NASAImageBackground(Renderable):
    img: str
    img_path: str
    width: int
    height: int
    local_paths: bool
    prng: Random

    def __init__(self,
                 w: int, 
                 h: int,
                 img: str,
                 local_paths: bool = False,
                 prng: Random = Random()) -> None:
        self.width = w
        self.height = h
        self.prng = prng
        self.img = img
        self.img_path = os.path.join(ASSET_DIR, img)
        self.local_paths = local_paths
    
    def render(self, dwg: Drawing) -> Group:
        width: int
        height: int

        with Image.open(self.img_path) as img:
            width, height = img.size

        max_x_scale = 1.0
        max_y_scale = 1.0
        min_x_scale = self.width / width
        min_y_scale = self.height / height

        min_scale = max(min_x_scale, min_y_scale)
        max_scale = min(max_x_scale, max_y_scale)
        scale = self.prng.uniform(min_scale, max_scale)

        min_x_translate = 0
        min_y_translate = 0
        max_x_translate = (width * scale) - self.width
        max_y_translate = (height * scale) - self.height

        image_url = "/assets/%s" % self.img
        if self.local_paths:
            image_url = "file://%s" % os.path.join(ASSET_DIR, self.img)

        g = dwg.g()
        r = dwg.image(href=self.img)
        r["xlink:href"] = image_url
        r["width"] = "%dpx" % width
        r["height"] = "%dpx" % height

        r.scale(scale)
        r.translate(self.prng.uniform(min_x_translate, - max_x_translate),
                    self.prng.uniform(min_y_translate, - max_y_translate))

        g.add(r)

        return g

def random_background(prng: Random, width: int, height: int, local_paths: bool = False) -> Renderable:
    images = [p for p in os.listdir(ASSET_DIR) if p.endswith(".jpg")]
    image = prng.choice(images)
    #image = "PIA03149~orig.jpg"

    return NASAImageBackground(width, height, image, local_paths, prng)