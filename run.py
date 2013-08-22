from PIL import Image
from transform import *
from loadobj import *
from loadtexture import *
from seamequilizer import *

def save_image(save_name, image):
    image.save(save_name)

def run(texture, original, modified, save_as):
    
    image, image_m, image_n = load_texture(texture)

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

    print "transforming"
    transformed_image = transform_img(image, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt, image_m,image_n)
    
    print "saving"

    #composite(save_as, transformed_image)

    #print "composited"

    save_image(save_as, transformed_image)
                         
    return "done"

#name of the texture, original, and modified model, and a name to save the modified texture
#have to be in the same directory, otherwise need to specify path
texture = "babyroshtext.png"
original = "babyrosh1.obj"
modified = "mayarosh.obj"
save_as = "output8.png"
run(texture,original,modified,save_as)
