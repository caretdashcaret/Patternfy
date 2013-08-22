from PIL import Image
#loads image
def load_texture(image_name):
    image = Image.open(image_name)
    image.load()
    
    #size
    m, n = image.size

    return [image, m, n]
