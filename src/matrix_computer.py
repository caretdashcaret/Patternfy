import numpy

class MatrixComputer():

    def __init__(self, source_pts, destination_pts):
        self.source_pts = source_pts
        self.destination_pts = destination_pts

    def get_transformations(self, transforming_triangles):
        transformation_matrices = []

        for source, destination in transforming_triangles:
            transformation_matrices.append(self.compute_transformation_matrix(source, destination))
        return  transformation_matrices

    def get_transforming_triangles(self):
        """only handles faces with 3 or 4 points"""
        triangles = []

        source_triangle = self.source_pts[0:3]
        destination_triangle = self.destination_pts[0:3]

        triangles.append((source_triangle, destination_triangle))

        if (len(self.source_pts)>3) and (len(self.destination_pts)>3):
            source_triangle = self.source_pts[2:]
            source_triangle.append(self.source_pts[0])

            destination_triangle = self.destination_pts[2:]
            destination_triangle.append(self.destination_pts[0])

            triangles.append((source_triangle, destination_triangle))

        return triangles

    def compute_transformation_matrix(self, source_triangle, destination_triangle):
        ((x11,x12), (x21,x22), (x31,x32)) = source_triangle
        ((y11,y12), (y21,y22), (y31,y32)) = destination_triangle

        M = numpy.array([
                         [y11, y12, 1, 0, 0, 0],
                         [y21, y22, 1, 0, 0, 0],
                         [y31, y32, 1, 0, 0, 0],
                         [0, 0, 0, y11, y12, 1],
                         [0, 0, 0, y21, y22, 1],
                         [0, 0, 0, y31, y32, 1]
                    ])

        y = numpy.array([x11, x21, x31, x12, x22, x32])

        #try-catch is to prevent singular matrices, it's a hack solution to just shift pixels by 1
        #singular matrices can occur because the point coordinates are mapped to the nearest integer pixel
        try:
            A = numpy.linalg.solve(M, y)
        except:
            M = numpy.array([
                         [y11, y12+1, 1, 0, 0, 0],
                         [y21, y22-1, 1, 0, 0, 0],
                         [y31, y32, 1, 0, 0, 0],
                         [0, 0, 0, y11, y12+1, 1],
                         [0, 0, 0, y21, y22-1, 1],
                         [0, 0, 0, y31, y32, 1]
                    ])
            y = numpy.array([x11, x21, x31, x12, x22, x32])
            A = numpy.linalg.solve(M, y)
        return A