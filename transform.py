import Image
from rectransform import *
import ImageDraw

def transform_img(channel, original_face_to_vts, original_vts, mod_face_to_vts, mod_vts, width, height):
    #depending on the new uvs, might have to alter the scale factor

    factor_w, factor_h = find_scaling_factors(original_vts, mod_vts)
    new_width, new_height = find_new_image_size(width, height, factor_w, factor_h)    
    new_image = Image.new("RGB", (new_width, new_height), "white")

    faces = len(original_face_to_vts)
    face_idx = 0

    while face_idx < faces:
        o_set = original_face_to_vts[face_idx]
        
        pts = [original_vts[int(i)-1] for i in o_set] 
        fx = [int(float(x[0])*width) for x in pts]

        fy = [map_within_range(float(y[1])) for y in pts]
        fy = [int((1-y) * height) for y in fy]        

        fp = zip(fx, fy)
        m_set = mod_face_to_vts[face_idx]

        mpts = [mod_vts[int(i)-1] for i in m_set] 
        
        tx = [int(float(x[0])*width) for x in mpts]
        ty = [int((1-float(y[1]))*height) for y in mpts]

        tp = zip(tx,ty)

        rec_transform(fp, tp, channel, new_image)
                
        face_idx += 1

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
