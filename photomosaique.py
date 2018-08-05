from PIL import Image, ImageFilter
from math import *
from norms import *

def create_mosaique(src, images, dims, sat) :
    
    #output = Image.new("RGB", (src.size[0] * images[0].size[0], src.size[1] * images[0].size[1]))
    output = Image.new("RGB", (src.size[0], src.size[1]))
    #src.copy()
    rgb = []

    # Calcul moyennes des teintes de chaques images (or source)
    for image in images :
        moy = average_rgb(image)
        rgb.append(moy)

    # On colle les images selon la comparaison des teintes
    index_rgb = []
    list_src_cut = cut_img(images, src, dims)
    for img_cut in list_src_cut :
        rgb_img_cut = average_rgb(img_cut)
        #buffer = img_cut.load()
        #pos = [x*images[0].size[0],y*images[0].size[1]]
        #r,g,b = buffer[x,y]
        index_rgb.append(calcul_diff(rgb_img_cut,rgb))
        

    i = 0
    pos = [0,0]
    
    for y in range(0,src.size[1],images[0].size[1]) :
        for x in range(0,src.size[0],images[0].size[0]) :
            output.paste(images[index_rgb[i]],pos)
            pos = [x,y]
            i += 1
            
    #dims = [512,512]
    #resize(output, dims)
    if(sat != ["n","n"]) :
        output = ajust_saturation(src, output, sat)
    return output
    pass

# On cherche l'index de l'image ayant la teinte la plus proche de la source
def calcul_diff(moy_rgb_src,rgb) :
    
    #moy_rgb_src = (r + g + b)/3
    val = 256
    index = 0
    count = 0
    for moy_rgb_images in rgb :
        moy_abs = sqrt((moy_rgb_src[0] - moy_rgb_images[0]) ** 2 + (moy_rgb_src[1] - moy_rgb_images[1]) ** 2 + 
        (moy_rgb_src[2] - moy_rgb_images[2]) ** 2)
        #moy_abs = (moy_rgb_src[0] - moy_rgb_images[0]) ** 2 + (moy_rgb_src[1] - moy_rgb_images[1]) ** 2 +(moy_rgb_src[2] - moy_rgb_images[2]) ** 2
        #moy_abs = abs(moy_rgb_images[0] - moy_rgb_src[0] + moy_rgb_images[1] - moy_rgb_src[1] + moy_rgb_images[2] - moy_rgb_src[2])
        #moy_abs = abs(moy_rgb_images - moy_rgb_src)
        count += 1
        if(val > moy_abs) :
            val = moy_abs
            index = count
    return index-1 
    pass

def crop(im, top, left, bottom, right):
    #cop = im.copy()
    imgMain = im.load()
    width = right - left
    height = bottom - top
    #print(width,height)
    
    if(im.mode == "RGB") :
        img = Image.new("RGB", (width,height))
    else : 
        img = Image.new("L", (width,height))
    buffer = img.load()
    
    sizeX = img.size[0]
    sizeY = img.size[1]

    #box =(left,top,right,bottom)
    #img = cop.crop(box)
    #print(left,top)
    #print(img.size[0],img.size[1])
    
    if left + sizeX >= im.size[0] :
        sizeX = im.size[0] - left
    if top + sizeY >= im.size[1] :
        sizeY = im.size[1] - top
    
    for y in range(sizeY) :
        for x in range(sizeX) :
            if(im.mode == "RGB") :
                #print(left + x,top + y)
                r,g,b = imgMain[left + x,top + y]
                #r,g,b = 255,130,245
                buffer[x,y] = r,g,b
            else : 
                v = imgMain[left + x,top + y]
                buffer[x,y] = v
    
    #img.show()
    return img       
    pass


# On subdivise l'image source selon les dimensions "dims"
def cut_img(images, src, dims) :
    output = []
    for y in range(0,src.size[1],images[0].size[1]) :
        for x in range(0,src.size[0],images[0].size[0]) :
            #if(x + images[0].size[0] < src.size[0] and y + images[0].size[1] < src.size[1]) :
            top = y
            left = x
            bottom = y + dims[1]
            right = x + dims[0]
            output.append(crop(src, top, left, bottom, right))
    return output
    pass


def average_rgb(image):
    average_red = 0
    average_green = 0
    average_blue = 0
    maxcolors = image.size[0]*image.size[1]
    colors = image.getcolors(maxcolors)
    for color in colors:
        average_red += color[1][0] * color[0]
        average_green += color[1][1] * color[0]
        average_blue += color[1][2] * color[0]
    average_red /= maxcolors
    average_green /= maxcolors
    average_blue /= maxcolors
    return (average_red, average_green, average_blue)

def ajust_saturation(src, output, sat) :
    src_hsv = src.convert("HSV")
    output_hsv = output.convert("HSV")
    b_src_hsv = src_hsv.load()
    b_output_hsv = output_hsv.load()
    for y in range(output_hsv.size[1]) :
        for x in range(output_hsv.size[0]) :
            hsrc,ssrc,vsrc = b_src_hsv[x,y]
            h,s,v = b_output_hsv[x,y]
            if(sat[0] == "y"):
                s = ssrc
            if(sat[1] == "y"):
                v = vsrc
            b_output_hsv[x,y] = h,s,v
    output = output_hsv.convert("RGB")
    return output
    pass
