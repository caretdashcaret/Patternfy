import unittest
from src import ObjectLoader
from src import TextureLoader
from src import SeamEquilizer
from src import ImageTransformer
from src import MatrixComputer
from PIL import ImageChops
from PIL import Image
import random
import os

class ImageTransformerTest(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        texture_filename = "objects/original_texture.png"
        texture = os.path.join(path, texture_filename)

        original_filename = "objects/original.obj"
        original = os.path.join(path, original_filename)

        modified_filename = "objects/modified.obj"
        modified = os.path.join(path, modified_filename)

        image = TextureLoader(texture).load_texture()
        original_face_to_vt, original_edges, original_vt = ObjectLoader(original).load_obj()
        modified_face_to_vt, modified_edges, modified_vt = ObjectLoader(modified).load_obj()
        SeamEquilizer(modified_edges, modified_vt).equilize()
        self.image_transformer = ImageTransformer(image, original_face_to_vt, original_vt, modified_face_to_vt, modified_vt)

        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.transformations = range(0, 12)
        self.face_transformations = range(0, 6)

    def test_map_within_range(self):
        mapped = self.image_transformer.map_within_range(250.5)
        assert mapped == 0.5

        random_number = random.random() * 10
        random_mapped = self.image_transformer.map_within_range(random_number)

        assert random_mapped <= 1.0

    def test_find_min_max(self):
        vts = [(1.0, 2.0), (3.0, 10.0)]
        result = self.image_transformer.find_min_max(vts)
        assert result == (2.0, 8.0)

    def test_find_scaling_factors(self):
        #based on loaded data
        factorw, factorh = self.image_transformer.find_scaling_factors()

        assert factorw == 1
        assert factorh == 2

    def test_find_new_image_size(self):
        new_width, new_height = self.image_transformer.find_new_image_size(10, 20)

        assert new_width == 10240
        assert new_height == 20480

    def test_get_img_pt_x(self):
        point = 0.2
        image_point = self.image_transformer.get_img_pt_x(point)
        assert image_point == 204

        point = 0.0
        image_point = self.image_transformer.get_img_pt_x(point)
        assert image_point == 0

    def test_get_img_pt_y(self):
        point = 0.2
        image_point = self.image_transformer.get_img_pt_y(point)
        assert image_point == 819

        point = 0.0
        image_point = self.image_transformer.get_img_pt_y(point)
        assert image_point == 1024

    def test_get_img_pts(self):
        points = [(0.2, 0.0)]
        image_points = self.image_transformer.get_img_pts(points)

        assert image_points == [(204, 1024)]

    def test_get_original_img_pts(self):
        points = [(2.2, 500.0)]
        image_points = self.image_transformer.get_original_img_pts(points)

        assert image_points == [(204, 1024)]

    def test_get_modified_img_pts(self):
        points = [(0.2, 0.0)]
        image_points = self.image_transformer.get_modified_img_pts(points)

        assert image_points == [(204, 1024)]

    def test_get_all_image_points(self):
        #this is from loaded data
        originial, modified = self.image_transformer.get_all_image_points(2)
        expected_original = [(260, 205), (378, 205), (378, 87), (260, 87)]
        expected_modified = [(318, 762), (404, 843), (485, 757), (399, 676)]

        assert originial == expected_original
        assert modified == expected_modified

    def test_apply_transformation_to_image(self):

        counter = 0
        self.image_transformer.modified_image = self.image_transformer.create_new_image()

        for original_face_idx, original_face in self.image_transformer.original_face_to_vts.items():
            original_image_points, modified_image_points = self.image_transformer.get_all_image_points(original_face_idx)
            matrix_computer = MatrixComputer(original_image_points, modified_image_points)
            sections = matrix_computer.get_transforming_triangles()
            matrices = matrix_computer.get_transformations(sections)

            for triangles, matrix in zip(sections, matrices):
                source_triangle, destination_triangle = triangles
                self.image_transformer.apply_transformation_to_image(source_triangle, destination_triangle, matrix)
                filename = self.get_apply_transformation_filename(counter)
                self.image_transformer.modified_image.save(filename)
                counter += 1

        for step_number in self.transformations:
            expected = self.get_expected_applied_filename(step_number)
            actual = self.get_apply_transformation_filename(step_number)
            self.assertTrue(self.image_equal(expected, actual), "transformation_" + str(step_number) + ".pngs are not equal ")

        self.teardown_apply_transformation_to_image()


    def get_apply_transformation_filename(self, step_num):
        transf_filename = "test/temp/transformation_" + str(step_num) + ".png"
        transf_file = os.path.join(self.path, transf_filename)
        return transf_file

    def get_expected_applied_filename(self, step_num):
        transf_filename = "objects/transformations/transformation_" + str(step_num) + ".png"
        transf_file = os.path.join(self.path, transf_filename)
        return transf_file

    def image_equal(self, im1_name, im2_name):
        im1 = Image.open(im1_name)
        im2 = Image.open(im2_name)
        return ImageChops.difference(im1, im2).getbbox() is None

    def teardown_apply_transformation_to_image(self):
        for transf in self.transformations:
            filename = self.get_apply_transformation_filename(transf)
            try: #need a better way to check for if file exists
                os.remove(filename)
            except:
                pass

    def test_transform_image_points(self):
        counter = 0
        self.image_transformer.modified_image = self.image_transformer.create_new_image()

        for original_face_idx, original_face in self.image_transformer.original_face_to_vts.items():
            original_image_points, modified_image_points = self.image_transformer.get_all_image_points(original_face_idx)
            self.image_transformer.transform_image_points(original_image_points, modified_image_points)
            filename = self.get_transform_imgpts_filename(counter)
            self.image_transformer.modified_image.save(filename)
            counter += 1

        for transformation in self.face_transformations:
            expected = self.get_expected_imgpts_filename(transformation)
            actual = self.get_transform_imgpts_filename(transformation)
            self.assertTrue(self.image_equal(expected, actual), "face_transformation_" + str(transformation) + ".pngs are not equal")

        self.teardown_transform_imgpts()

    def get_transform_imgpts_filename(self, step_num):
        transf_filename = "test/temp/face_transformation_" + str(step_num) + ".png"
        transf_file = os.path.join(self.path, transf_filename)
        return transf_file

    def get_expected_imgpts_filename(self, step_num):
        transf_filename = "objects/face_transformations/face_transformation_" + str(step_num) + ".png"
        transf_file = os.path.join(self.path, transf_filename)
        return transf_file

    def teardown_transform_imgpts(self):
        for transf in self.face_transformations:
            filename = self.get_transform_imgpts_filename(transf)
            try: #need a better way to check for if file exists
                os.remove(filename)
            except:
                pass
