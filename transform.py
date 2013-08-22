import Image
from rectransform import *
import ImageDraw

def transform_img(channel, original_face_to_vts, original_vts, mod_face_to_vts, mod_vts, width, height ):
    #depending on the new uvs, might have to alter the scale factor
    factorw = 3
    factorh = 2
    new_image = Image.new("RGB", (int(width)*factorw,int(height)*factorh), "white")

    faces = len(original_face_to_vts)
    face_idx = 0

    while face_idx < faces:
        o_set = original_face_to_vts[face_idx]
        
        pts = [original_vts[int(i)-1] for i in o_set] 
        fx = [int(float(x[0])*width) for x in pts]
        fy = [int((-1*float(y[1]))*height) for y in pts]

        fp = zip(fx, fy)
        m_set = mod_face_to_vts[face_idx]

        mpts = [mod_vts[int(i)-1] for i in m_set] 
        
        tx = [int(float(x[0])*width) for x in mpts]
        ty = [int((1-float(y[1]))*height) for y in mpts]

        tp = zip(tx,ty)

        rec_transform(fp, tp, channel, new_image)
                
        face_idx += 1

    return new_image
