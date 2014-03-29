from src.transform import *
from src import ObjectLoader
from src import TextureLoader
from src import SeamEquilizer

def save_image(save_name, image):
    image.save(save_name)

def run(texture, original, modified, save_as):
    
    image, image_m, image_n = TextureLoader(texture).load_texture()

    print "texture loaded"

    #load obj with original uvs
    original_face_to_vt, original_edges, original_vt = ObjectLoader(original).load_obj()

    print "original uvs"

    #load obj with modified uvs
    modified_face_to_vt, modified_edges, modified_vt = ObjectLoader(modified).load_obj()

    print "mod uvs"
    
    #equilize seams
    SeamEquilizer(modified_edges, modified_vt).equilize()

    print "seam equilized"

    print "transforming"
    transformed_image = transform_img(image, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt, image_m,image_n)
    
    print "saving"

    save_image(save_as, transformed_image)
                         
    return "done"

#name of the texture, original, and modified model, and a name to save the modified texture
#have to be in the same directory, otherwise need to specify path

