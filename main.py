import os
from pathlib import Path
from PIL import Image
import numpy as np

BASE_DIR = Path(__file__).parent

INPUT_DIR = BASE_DIR / "raw"
OUT_DIR = BASE_DIR / "out"


def auto_crop(path, name):
    im = Image.open(path)
    w, h = im.size

    a = np.asarray(im)

    least_x = w
    most_x = 0
    least_y = h
    most_y = 0

    found_start_y = False

    for y in range(h):
        found_start_x = False
        empty_row = True
        for x in range(w):
            is_alpha = True
            for i in a[y, x]:
                if i != 0:
                    is_alpha = False
                    empty_row = False
                    break

            if not is_alpha:
                if found_start_x:
                    if x > most_x:
                        most_x = x
                else:
                    if x < least_x:
                        least_x = x
                        found_start_x = True

        if not empty_row:
            if found_start_y:
                if y > most_y:
                    most_y = y
            else:
                if y < least_y:
                    least_y = y
                    found_start_y = True

    im1 = im.crop((least_x, least_y, most_x, most_y))
    im1.save(OUT_DIR / (name + ".png"), format="PNG")


for file in os.listdir(INPUT_DIR):
    [name, ext] = file.split(".")
    if ext == "png":
        auto_crop(INPUT_DIR / file, name)
