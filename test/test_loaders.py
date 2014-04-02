import unittest
from src import TextureLoader
from src import ObjectLoader
import os
import PIL

class TextureLoaderTest(unittest.TestCase):

    def test_load_texture(self):

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "objects/original_texture.png"
        file_location = os.path.join(path, filename)

        new_texture = TextureLoader(file_location)
        image = new_texture.load_texture()

        assert isinstance(image, PIL.PngImagePlugin.PngImageFile)

class ObjectLoaderTest(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "objects/original.obj"
        file_location = os.path.join(path, filename)

        self.loader = ObjectLoader(file_location)

    def test_load_object(self):
        f_to_vts, edges_to_vts, vts = self.loader.load_obj()

        expected_vts = [[0.189, 0.6133], [0.189, 0.729], [0.0733, 0.729], [0.0733, 0.6133], [0.073, 0.8024], [0.1887, 0.8024], [0.1887, 0.9181], [0.073, 0.9181], [0.254, 0.7993], [0.3697, 0.7993], [0.3697, 0.915], [0.254, 0.915], [0.4426, 0.7869], [0.5583, 0.7869], [0.5583, 0.9026], [0.4426, 0.9026], [0.6388, 0.789], [0.7545, 0.789], [0.7545, 0.9047], [0.6388, 0.9047], [0.8142, 0.801], [0.9299, 0.801], [0.9299, 0.8763], [0.8142, 0.8763]]
        expected_edges_to_vts = {(1, 2): [[1, 2], [22, 21]], (7, 8): [[7, 8], [20, 19]], (6, 7): [[6, 7], [16, 15]], (4, 6): [[10, 11], [13, 16]], (5, 6): [[5, 6], [12, 11]], (4, 1): [[4, 1], [10, 9]], (2, 8): [[18, 19], [21, 24]], (8, 5): [[8, 5], [24, 23]], (2, 3): [[2, 3], [18, 17]], (3, 7): [[14, 15], [17, 20]], (5, 1): [[12, 9], [23, 22]], (3, 4): [[3, 4], [14, 13]]}
        expected_f_to_vts = {0: [1, 2, 3, 4], 1: [5, 6, 7, 8], 2: [9, 10, 11, 12], 3: [13, 14, 15, 16], 4: [17, 18, 19, 20], 5: [21, 22, 23, 24]}

        assert f_to_vts == expected_f_to_vts
        assert edges_to_vts == expected_edges_to_vts
        assert vts == expected_vts

    def test_read_obj_file(self):
        vts, faces = self.loader.read_obj_file()

        expected_vts = [[0.189, 0.6133], [0.189, 0.729], [0.0733, 0.729], [0.0733, 0.6133], [0.073, 0.8024], [0.1887, 0.8024], [0.1887, 0.9181], [0.073, 0.9181], [0.254, 0.7993], [0.3697, 0.7993], [0.3697, 0.915], [0.254, 0.915], [0.4426, 0.7869], [0.5583, 0.7869], [0.5583, 0.9026], [0.4426, 0.9026], [0.6388, 0.789], [0.7545, 0.789], [0.7545, 0.9047], [0.6388, 0.9047], [0.8142, 0.801], [0.9299, 0.801], [0.9299, 0.8763], [0.8142, 0.8763]]
        expected_faces = [[[1, 1, 1], [2, 2, 1], [3, 3, 1], [4, 4, 1]], [[5, 5, 2], [6, 6, 2], [7, 7, 2], [8, 8, 2]], [[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]], [[4, 13, 4], [3, 14, 4], [7, 15, 4], [6, 16, 4]], [[3, 17, 5], [2, 18, 5], [8, 19, 5], [7, 20, 5]], [[2, 21, 6], [1, 22, 6], [5, 23, 6], [8, 24, 6]]]

        assert vts == expected_vts
        assert faces == expected_faces

    def test_parse_coordinates(self):
        test_string = "vt 0.1887 0.8024 0.0000"
        parsed_result = self.loader.parse_coordinates(test_string)

        assert parsed_result == [0.1887, 0.8024]

    def test_parse_face(self):
        test_string = "f 1/9/3 4/10/3 6/11/3 5/12/3"
        parsed_result = self.loader.parse_face(test_string)

        assert parsed_result == [[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]]

    def test_extract_vt_index(self):
        test_face = [[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]]
        extracted_vt_index = self.loader.extract_vt_index(test_face)

        assert extracted_vt_index == [9, 10, 11, 12]

    def test_map_faces_to_vts(self):
        test_faces = [[[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]],[[1, 1, 3], [4, 2, 3], [6, 3, 3], [5, 4, 3]]]
        f_to_vts = self.loader.map_faces_to_vts(test_faces)
        expected_f_to_vts = {0:[9, 10, 11, 12], 1:[1, 2, 3, 4]}

        assert f_to_vts == expected_f_to_vts

    def test_parse_edges(self):
        test_face = [[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]]
        edges_to_vts = {}
        edges_to_vts = self.loader.parse_edges(test_face, edges_to_vts)

        expected_edges_to_vts = {(5, 1): [[12, 9]], (6, 5): [[11, 12]], (4, 6): [[10, 11]], (1, 4): [[9, 10]]}
        assert edges_to_vts == expected_edges_to_vts

        test_additional_face = [[5, 90, 3], [1, 120, 3]]
        edges_to_vts = self.loader.parse_edges(test_additional_face, edges_to_vts)

        expected_edges_to_vts = {(5, 1): [[12, 9], [90, 120]], (6, 5): [[11, 12]], (4, 6): [[10, 11]], (1, 4): [[9, 10]]}
        assert edges_to_vts == expected_edges_to_vts

    def test_map_edges_to_vts(self):
        test_faces = [[[1, 9, 3], [4, 10, 3], [6, 11, 3], [5, 12, 3]], [[1, 90, 3], [5, 120, 3]]]
        edges_to_vts = self.loader.map_edges_to_vts(test_faces)
        expected_edges_to_vts = {(5, 1): [[12, 9], [120, 90]], (6, 5): [[11, 12]], (4, 6): [[10, 11]], (1, 4): [[9, 10]]}

        assert edges_to_vts == expected_edges_to_vts