import os
from PIL import Image


def find_img(directory) -> list[Image.Image]:
    images = []
    for element in os.listdir(directory):
        if os.path.isdir(element):
            pass
        else:
            img = Image.open(directory + element)
            images.append(img.convert("RGB"))
    return images
