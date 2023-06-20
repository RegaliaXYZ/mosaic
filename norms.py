from PIL import Image, ImageFilter


def normalize(images: list, dims: list[int]) -> list[Image.Image]:
    normalized_images = []

    for i in range(len(images)):
        normalized_images.append(resize(images[i], dims))

    return normalized_images


def resize(src_img: Image.Image, dims: list[int]) -> Image.Image:

    out_img = Image.new("RGB", (dims[0], dims[1]))
    new_image = out_img.load()
    old_image = src_img.load()

    ratioX = src_img.size[0] / out_img.size[0]
    ratioY = src_img.size[1] / out_img.size[1]

    for y in range(out_img.size[1]):
        for x in range(out_img.size[0]):
            X = int(x*ratioX)
            Y = int(y*ratioY)
            new_image[x, y] = old_image[X, Y]

    return out_img
