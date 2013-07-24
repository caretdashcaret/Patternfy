from PIL import Image
from scipy import ndimage
from scipy import misc
from scipy import nditer
from transform import *
from loadobj import *
from loadtexture import *
from seamequilizer import *

def composite(save_name, channels):
    img = Image.merge("RGB", channels)
    img.save(save_name)

def run():
    #name of the texture, original, and modified model
    #have to be in the same directory, otherwise need to specify path
    texture = "babyroshtext.png"
    original = "babyrosh.obj"
    modified = "modifiedbabyrosh.obj"

    #channel R,G,B
    ch0, ch1, ch2, image_m, image_n = load_texture(texture)

    print "texture loaded"

    #load obj with original uvs
    original_face_to_vt, e1, original_vt = load_obj(original)

    print "original uvs"

    #load obj with modified uvs
    modified_face_to_vt, e2, modified_vt = load_obj(modified)

    print "mod uvs"
    
    #equilize seams
    seam_equilize(e2, modified_vt)

    print "seam equilized"

    #transform & composite
    channels = [ch0, ch1, ch2]
    transformed_image = []
    for ch in channels:
        print "transforming " + str(channels.index(ch))
        transformed_image.append(transform_img(ch, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt, image_m,image_n))

    
    print "transformed"

    save_as = "output.png"

    composite(save_as, transformed_image)

    print "composited"
                         
    return "done"

run()
