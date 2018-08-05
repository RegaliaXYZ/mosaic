from PIL import Image, ImageFilter
from norms import *
from loader import *
from photomosaique import *
import time

def main() :
    directoryImages = "images/"
    directoryInputs = "inputs/"
    directoryOutputs = "./outputs/"
    input_load = find_img(directoryInputs)
    for image in input_load :
        try :
            path = directoryInputs + image
            print(path)
        except :
            print("Unable to load image")
    
    fileToOpen = input("Entrez le nom du fichier à transformer: ")
    extension = input("Quelle est l'extension du fichier? ")
    sub = int(input("Entrez le nombre de subdivision de l'image : "))
    sat = ["n","n"]
    sat[0] = input("Ajuster la saturation (y/n) ? ")
    sat[1] = input("Ajuster la lightness (y/n) ? ")
    src= Image.open(directoryInputs + fileToOpen + "." + extension)
    src = src.convert("RGB")
    images = []
    img_load = find_img(directoryImages)
    for image in img_load :
        try :
            path = directoryImages + image
            im = Image.open(path)
            images.append(im.convert("RGB"))
        except :
            print("Unable to load image")
    dims = [src.size[0] // sub, src.size[1] // sub]
    images = normalize(images, dims)
    output = create_mosaique(src,images,dims,sat)
    if(sat[0]=="y"):
        if(sat[1]=="y"):
            output.save(directoryOutputs + fileToOpen + "_" + str(sub) + "_" + "WL_WS.jpg","JPEG")
        else:
            output.save(directoryOutputs + fileToOpen + "_" + str(sub) + "_" + "SL_WS.jpg","JPEG")
    else:
        if(sat[1]=="y"):
            output.save(directoryOutputs + fileToOpen + "_" + str(sub) + "_" + "WL_SS.jpg","JPEG")
        else:
            output.save(directoryOutputs + fileToOpen + "_" + str(sub) + "_" + "SL_SS.jpg","JPEG")

    #output.show()
    pass


if __name__ == "__main__" :
    start_time  = time.time()
    main()
    end_time = time.time()
    print("Programme execute en " + str(int(end_time - start_time)) + " !")
    pass
