import Image
import ImageDraw
import numpy

#transformation
#most of the code copied from StackOverflow, with modifications
def transformblit(src_tri, dst_tri, src_img, dst_img):
    A = compute_transformation_matrix(src_tri, dst_tri)

    src_copy = src_img.copy()
    srcdraw = ImageDraw.Draw(src_copy)
    srcdraw.polygon(src_tri)

    transformed = src_img.transform(dst_img.size, Image.AFFINE, A)

    #image mask
    mask = Image.new('1', dst_img.size)
    maskdraw = ImageDraw.Draw(mask)
    maskdraw.polygon(dst_tri, fill=255)

    dstdraw = ImageDraw.Draw(dst_img)
    dstdraw.polygon(dst_tri, fill=255)

    #paste final transformed image
    dst_img.paste(transformed, mask=mask)

def compute_transformation_matrix(source_triangle, destination_triangle):
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

#faces are split into triangles for transformation, only handles for faces up to 4 points
def rec_transform(src_tri, dst_tri, src_img, dst_img):
    tri11 = src_tri[0:3]
    tri21 = dst_tri[0:3]
    transformblit(tri11, tri21, src_img, dst_img)
    
    if (len(src_tri)>3) and (len(dst_tri)>3):
        tri12 = src_tri[2:]
        tri12.append(src_tri[0])
        tri22 = dst_tri[2:]
        tri22.append(dst_tri[0])

        transformblit(tri12, tri22, src_img, dst_img)
