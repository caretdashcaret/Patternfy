from PIL import Image
from scipy import *
#loads image
def load_texture(image_name):
    image = Image.open(image_name)
    im = array(image)
    
    #size
    m, n = image.size
    
    #color channels
    red, green, blue = image.split()
        
    return [red, green, blue, m, n]
