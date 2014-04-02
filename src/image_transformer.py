import Image
import ImageDraw
import numpy
from matrix_computer import MatrixComputer

class ImageTransformer():

    def __init__(self, original_image, original_face_to_vts, original_vts, mod_face_to_vts, mod_vts):
        self.original_image = original_image
        self.original_face_to_vts = original_face_to_vts
        self.original_vts = original_vts
        self.mod_face_to_vts = mod_face_to_vts
        self.modified_vts = mod_vts
        self.width, self.height = original_image.size
        self.modified_image = None

    def transform(self):
        """creates a new image and transforms the triangles from the old image to the new image"""

        self.modified_image = self.create_new_image()
        self.transform_faces()

        return self.modified_image

    def create_new_image(self):
        factor_w, factor_h = self.find_scaling_factors()
        new_width, new_height = self.find_new_image_size(factor_w, factor_h)
        new_image = Image.new("RGB", (new_width, new_height), "white")

        return new_image

    def map_within_range(self, number):
        return number - numpy.floor(number)

    def find_min_max(self, vts):
        y_coords = [vt[1] for vt in vts]
        x_coords = [vt[0] for vt in vts]

        return max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)

    def find_scaling_factors(self):
        orignal_vts_width, original_vts_height = self.find_min_max(self.original_vts)
        modified_vts_width, modified_vts_height = self.find_min_max(self.modified_vts)

        factor_w = numpy.ceil(modified_vts_width / orignal_vts_width)
        factor_h = numpy.ceil(modified_vts_height / original_vts_height)

        return factor_w, factor_h

    def find_new_image_size(self, factor_w, factor_h):
        new_width = int(self.width * factor_w)
        new_height = int(self.height * factor_h)
        return new_width, new_height

    def transform_faces(self):

        for original_face_idx, original_face in self.original_face_to_vts.items():
            original_image_points, modified_image_points = self.get_all_image_points(original_face_idx)
            self.transform_image_points(original_image_points, modified_image_points)

    #the getting image points from coords is a little tricky because UVs (vts) have 0,0 as lower left corner
    #and PIL Image has 0,0 as the upper left corner
    #vts on the orignal model obey the UV definition and are mapped back between 0 and 1 to get the proper coordinate on
    #the original texture
    #that rule is disobeyed in the modified model, and can result in larger, non-square textures, which is good for
    #pattern drafting but bad for reconstructing the original UV mapping
    def get_img_pt_x(self, point):
        return int(point*self.width)

    def get_img_pt_y(self, point):
        return int((1-point)*self.height)

    def get_img_pts(self, pts):
        return [(self.get_img_pt_x(x), self.get_img_pt_y(y)) for x, y in pts]

    def get_original_img_pts(self, pts):
        fx = [(self.map_within_range(x), self.map_within_range(y)) for x, y in pts]
        return self.get_img_pts(fx)

    def get_modified_img_pts(self, pts):
        return self.get_img_pts(pts)

    def get_all_image_points(self, index):
        original_face = self.original_face_to_vts[index]
        pts = [self.original_vts[i-1] for i in original_face]
        orignal_image_points = self.get_original_img_pts(pts)

        corresponding_modified_face = self.mod_face_to_vts[index]
        modified_pts = [self.modified_vts[i-1] for i in corresponding_modified_face]
        modified_image_points = self.get_modified_img_pts(modified_pts)

        return orignal_image_points, modified_image_points

    def transform_image_points(self, original_image_points, modified_image_points):
        matrix_computer = MatrixComputer(original_image_points, modified_image_points)
        sections = matrix_computer.get_transforming_triangles()
        matrices = matrix_computer.get_transformations(sections)

        for triangles, matrix in zip(sections, matrices):
            source_triangle, destination_triangle = triangles
            self.apply_transformation_to_image(source_triangle, destination_triangle, matrix)

    def apply_transformation_to_image(self, source_triangle, destination_triangle, transformation):

        source_image_copy = self.original_image.copy()
        source_image_draw = ImageDraw.Draw(source_image_copy)
        source_image_draw.polygon(source_triangle)

        transformed = self.original_image.transform(self.modified_image.size, Image.AFFINE, transformation)

        #image mask
        mask = Image.new('1', self.modified_image.size)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.polygon(destination_triangle, fill=255)

        destination_draw = ImageDraw.Draw(self.modified_image)
        destination_draw.polygon(destination_triangle, fill=255)

        #paste final transformed image
        self.modified_image.paste(transformed, mask=mask)