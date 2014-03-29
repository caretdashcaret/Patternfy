import Image
from rectransform import *
import ImageDraw

def transform_img(original_image, original_face_to_vts, original_vts, mod_face_to_vts, mod_vts, width, height):
    #depending on the new uvs, might have to alter the scale factor

    factor_w, factor_h = find_scaling_factors(original_vts, mod_vts)
    new_width, new_height = find_new_image_size(width, height, factor_w, factor_h)    
    new_image = Image.new("RGB", (new_width, new_height), "white")

    transform_faces(original_face_to_vts, mod_face_to_vts, original_image, new_image, original_vts, mod_vts, width, height)

    return new_image

def map_within_range(number):
    return number - numpy.floor(number)

def find_min_max(vts):
    y_coords = [vt[1] for vt in vts]
    x_coords = [vt[0] for vt in vts]

    return max(x_coords) - min(x_coords), max(y_coords) - min(y_coords)

def find_scaling_factors(original_vts, modified_vts):
    orignal_vts_width, original_vts_height = find_min_max(original_vts)
    modified_vts_width, modified_vts_height = find_min_max(modified_vts)

    factor_w = numpy.ceil(modified_vts_width / orignal_vts_width)
    factor_h = numpy.ceil(modified_vts_height / original_vts_height)

    return factor_w, factor_h

def find_new_image_size(original_width, original_height, factor_w, factor_h):
    new_width = int(original_width * factor_w)
    new_height = int(original_height * factor_h)
    return new_width, new_height

def transform_faces(original_face_to_vts, mod_face_to_vts, original_img, new_img, original_vts, mod_vts, width, height):

    for original_face_idx, original_face in original_face_to_vts.items():
        pts = [original_vts[i-1] for i in original_face]
        fp = get_original_img_pts(pts, width, height)

        corresponding_modified_face = mod_face_to_vts[original_face_idx]
        modified_pts = [mod_vts[i-1] for i in corresponding_modified_face]
        tp = get_modified_img_pts(modified_pts, width, height)

        rec_transform(fp, tp, original_img, new_img)

def get_img_pt_x(point, width):
    return int(point*width)

def get_img_pt_y(point, height):
    return int((1-point)*height)

def get_img_pts(pts, width, height):
    return [(get_img_pt_x(x, width), get_img_pt_y(y, height)) for x, y in pts]

def get_original_img_pts(pts, width, height):
    fx = [(map_within_range(x), map_within_range(y)) for x, y in pts]
    return get_img_pts(fx, width, height)

def get_modified_img_pts(pts, width, height):
    return get_img_pts(pts, width, height)