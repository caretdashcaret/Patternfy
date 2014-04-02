import unittest
from src import ObjectLoader
from src import TextureLoader
from src import SeamEquilizer
from src import ImageTransformer
from PIL import ImageChops, Image
import os

class PatternfyTest(unittest.TestCase):

    def test_patternfy(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        texture_filename = "objects/original_texture.png"
        texture = os.path.join(path, texture_filename)

        original_filename = "objects/original.obj"
        original = os.path.join(path, original_filename)

        modified_filename = "objects/modified.obj"
        modified = os.path.join(path, modified_filename)

        save_filename = "test/output.png"
        save = os.path.join(path, save_filename)

        image = TextureLoader(texture).load_texture()
        original_face_to_vt, original_edges, original_vt = ObjectLoader(original).load_obj()
        modified_face_to_vt, modified_edges, modified_vt = ObjectLoader(modified).load_obj()
        SeamEquilizer(modified_edges, modified_vt).equilize()
        image_transformer = ImageTransformer(image, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt)
        transformed_image = image_transformer.transform()
        transformed_image.save(save)

        expected_filename = "objects/expected_output.png"
        expected = os.path.join(path, expected_filename)

        output_image = Image.open(save)
        output_image.load()
        expected_image = Image.open(expected)
        expected_image.load()

        assert self.image_equal(output_image, expected_image)

    def image_equal(self, im1, im2):
        return ImageChops.difference(im1, im2).getbbox() is None

    def tearDown(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        save_filename = "test/output.png"
        save = os.path.join(path, save_filename)

        os.remove(save)





