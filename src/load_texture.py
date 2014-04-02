from PIL import Image

class TextureLoader():
    """loads the image texture associated with the original OBJ"""

    def __init__(self, image_name):
        self.image_name = image_name

    def load_texture(self):
        image = Image.open(self.image_name)
        return image
