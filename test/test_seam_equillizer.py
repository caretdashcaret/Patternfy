import unittest
from src import ObjectLoader
from src import SeamEquilizer
import os
import random

class SeamEquilizerTest(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "objects/modified.obj"
        file_location = os.path.join(path, filename)
        new_object = ObjectLoader(file_location)
        f_to_vts, edges_to_vts, vts = new_object.load_obj()

        self.equilizer = SeamEquilizer(edges_to_vts, vts)

    def test_equilize(self):
        self.equilizer.equilize()
        expected_vts = [[0.7972, 0.2545], [0.8087, 0.1295], [0.9966, 0.2297], [0.8993, 0.3089], [0.3122, 0.45], [0.3972, 0.374], [0.5125, 0.4236], [0.3608, 0.5756], [0.311, 0.2555], [0.3949, 0.1759], [0.4745, 0.2599], [0.3906, 0.3395], [0.5544, 0.4604], [0.5973, 0.3425], [0.7585, 0.4821], [0.6358, 0.5421], [0.5258, 0.1355], [0.7387, 0.1355], [0.7387, 0.3484], [0.5258, 0.3484], [0.7679, 0.5076], [0.8155, 0.3915], [0.9312, 0.3904], [0.9808, 0.5057]]
        assert self.equilizer.vts == expected_vts

    def test_scale_variant_edge(self):
        edge_variants ={(5, 1): [[12, 9], [10, 11]]}
        self.equilizer.scale_variant_edge(edge_variants, 10)

        expected_vts = [[5.1763, -1.5558], [0.8516, 0.1524], [0.9537, 0.2068], [0.8993, 0.3089], [-4.0652, 2.2646], [0.3972, 0.374], [0.4775, 0.4573], [0.3941, 0.5376], [0.311, 0.2555], [0.3949, 0.1759], [0.4745, 0.2599], [0.3906, 0.3395], [0.5547, 0.4595], [0.6338, 0.375], [0.7183, 0.4541], [0.6392, 0.5385], [0.5258, 0.1355], [0.7387, 0.1355], [0.7387, 0.3484], [0.5258, 0.3484], [0.8367, 0.507], [0.8357, 0.3913], [0.911, 0.3906], [0.912, 0.5063]]

        assert self.equilizer.vts == expected_vts

    def test_find_lengths_of_edge_variants(self):
        edges = {(5, 1): [[12, 9], [120, 90]], (6, 5): [[11, 12]], (4, 6): [[10, 11]], (1, 4): [[9, 10]]}
        result = self.equilizer.find_lengths_of_edge_variants(edges)
        expected = {'(5, 1)': 0.5229712515999326, '(6, 5)': 0.11570211752599861, '(4, 6)': 0.5063026960228436, '(1, 4)': 0.11568824486524114}

        assert result == expected

    def test_set_new_vts_values(self):
        value_a = 100.0
        value_b = 200.0
        edge = [1, 2] #not a real edge, but valid for lookups

        self.equilizer.set_new_vts_values(value_a, value_b, edge)

        assert self.equilizer.vts[0] == value_a
        assert self.equilizer.vts[1] == value_b

    def test_get_vts_values(self):
        test_edge_variant = [5, 4] #not a real edge but will do a valid lookup in self.equilizer's vts
        result = self.equilizer.get_vts_values(test_edge_variant)

        assert result == ([0.3139, 0.4543], [0.8993, 0.3089])

    def test_get_vts_index_for_edge(self):
        test_edge_variant = [5, 4]
        result = self.equilizer.get_vts_index_for_edge(test_edge_variant)

        assert result == (4, 3)

    def test_scale(self):
        pt_a = (4.0, 2.0)
        pt_b = (-6.0, -6.0)
        factor = 10.0

        result = self.equilizer.scale(pt_a, pt_b, factor)
        expected = ([2.9043, 1.1235], [-4.9043, -5.1235])

        assert result == expected

    def test_midpoint(self):
        pt_a = (5, 2)
        pt_b = (-5, 2)

        assert self.equilizer.midpoint(pt_a, pt_b) == [0.0, 2.0]

    def test_euclidean_dist(self):
        pt_a = (5, 2)
        pt_b = (random.random() * -10, random.random() * -2)
        pt_c = (-5, 2)

        random_result = self.equilizer.euclidean_dist(pt_a, pt_b)
        assert random_result == self.equilizer.euclidean_dist(pt_b, pt_a)
        assert random_result > 0

        result = self.equilizer.euclidean_dist(pt_a, pt_c)
        assert result == 10

