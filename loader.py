import os

def find_img(directory):
    images = []
    for element in os.listdir(directory):
        if os.path.isdir(element):
            pass 
        else:
            images.append(element)
    return images
    pass
