from PIL import Image
from norms import *
from loader import *
from photomosaique import *
import time


def main():
    directoryImages = "source_images/"
    directoryInputs = "imgs_to_process/"
    directoryOutputs = "./outputs/"
    image_to_process: str = input(
        "Entrez le nom du fichier à transformer (test.png or test.jpg): ")
    # check if image exists in directory
    parts = image_to_process.split(".")
    if (len(parts) != 2):
        print("Invalid file name, exiting...")
        return
    if (parts[1] != "png" and parts[1] != "jpg"):
        print("Invalid file extension, exiting...")
        return
    if not os.path.exists(directoryInputs + image_to_process):
        print("File not found, exiting...")
        return

    # Get Mosaic specific parameters like number of subdivisions, saturation and lightness
    sub: int = int(input("Entrez le nombre de subdivision de l'image : "))
    saturation: bool = False
    saturation_input = input("Ajuster la saturation (y/N) ? ")
    if (saturation_input == "y"):
        saturation = True

    lightness: bool = False
    lightness_input = input("Ajuster la lightness (y/N) ? ")
    if (lightness_input == "y"):
        lightness = True

    # Get the image to process & convert it to RGB
    src_to_process = Image.open(directoryInputs + parts[0] + "." + parts[1])
    src_to_process = src_to_process.convert("RGB")

    # Get the images to use for the mosaic
    images: list[Image.Image] = find_img(directoryImages)

    # Normalize the images to the same size as the subdivisions
    dims = [src_to_process.size[0] // sub, src_to_process.size[1] // sub]
    images: list[Image.Image] = normalize(images, dims)

    # Create the mosaic
    output = create_mosaique(src_to_process, images,
                             dims, saturation, lightness)
    suffix = "WL_" if lightness else "SL_"
    suffix += "WS" if sat else "SS"
    ext = ".png" if parts[1] == "png" else ".jpg"
    ext_cap = "PNG" if parts[1] == "png" else "JPEG"
    output.save(directoryOutputs + parts[0] + "_" +
                str(sub) + "_" + suffix + ext, ext_cap)
    # exit program
    return


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print("Execution time: " + str(end_time - start_time) + " seconds")
