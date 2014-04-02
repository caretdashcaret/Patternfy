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

        save_filename = "test/temp/output.png"
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

        self.assertTrue(self.image_equal(save, expected), expected_filename + " and " + save_filename + " are not equal")

    def image_equal(self, im1_name, im2_name):
        im1 = Image.open(im1_name)
        im2 = Image.open(im2_name)
        return ImageChops.difference(im1, im2).getbbox() is None

    def tearDown(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        save_filename = "test/temp/output.png"
        save = os.path.join(path, save_filename)

        os.remove(save)





