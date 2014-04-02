import unittest
from src import MatrixComputer

class MatrixComputerTest(unittest.TestCase):

    def setUp(self):
        #the points are picked because they're a simple translation
        source_pts = [(0.0,0.0), (1.0,0.0), (1.0,1.0), (0.0, 1.0)]
        destination_pts = [(1.0,0.0), (2.0,0.0), (2.0,1.0), (1.0, 1.0)]

        self.computer = MatrixComputer(source_pts, destination_pts)

    def test_get_transforming_triangles(self):
        results = self.computer.get_transforming_triangles()
        expected_results = [([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)], [(1.0, 0.0), (2.0, 0.0), (2.0, 1.0)]), ([(1.0, 1.0), (0.0, 1.0), (0.0, 0.0)], [(2.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]
        assert results == expected_results
        assert len(results) == 2

    def test_compute_transformation_matrix(self):
        source_point = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0))
        destination_point = ((1.0, 0.0), (2.0, 0.0), (2.0, 1.0))
        result = self.computer.compute_transformation_matrix(source_point, destination_point)

        #the transformation maxtrix should be a column matrix:
        # [1.0
        # 0
        # -1.0
        # 0
        # 1.0
        # 0]

        assert result[0] == 1.0
        assert result[1] == 0.0
        assert result[2] == -1.0
        assert result[3] == 0
        assert result[4] == 1.0
        assert result[5] == 0

    def test_get_transformations(self):
        transforming_triangles = [([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)], [(1.0, 0.0), (2.0, 0.0), (2.0, 1.0)]), ([(1.0, 1.0), (0.0, 1.0), (0.0, 0.0)], [(2.0, 1.0), (1.0, 1.0), (1.0, 0.0)])]
        transformations = self.computer.get_transformations(transforming_triangles)

        assert len(transforming_triangles) == len(transformations)