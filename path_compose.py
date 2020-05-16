import sys
import os

dirname = os.path.dirname(__file__)

def rel_path(image_desc):         #function for composing absolute path to some image, given image number or name in different formats
    if type(image_desc) is int:
        path = os.path.join(dirname, "image" + str(image_desc) + ".png")
    elif type(image_desc) is str:
        if image_desc[-4:] == ".png":
            path = os.path.join(dirname, image_desc)
        else:
            path = os.path.join(dirname, image_desc + ".png")
    else:
        print("invalid image description!")
        sys.exit()
    return path