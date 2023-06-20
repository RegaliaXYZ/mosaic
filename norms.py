from PIL import Image, ImageFilter


def normalize(images: list, dims: list[int]) -> list[Image.Image]:

    maxH = 0
    minH = images[0].size[0]
    maxW = 0
    minW = images[0].size[1]
    newImages = []

    for i in range(len(images)):
        newImages.append(resize(images[i], dims))

    return newImages


def resize(im, dims):

    img = Image.new("RGB", (dims[0], dims[1]))
    new = img.load()
    old = im.load()

    ratioX = im.size[0] / img.size[0]
    ratioY = im.size[1] / img.size[1]

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            X = int(x*ratioX)
            Y = int(y*ratioY)
            new[x, y] = old[X, Y]

    return img
