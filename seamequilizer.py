import math

#makes sure seams are of equal length for reassembly
def seam_equilize(edges, vts):
    
    for edge in edges.keys():
        edge_variants = edges[edge]
        variant_to_length = {}
        for variant in edge_variants:
           variant_to_length[str(variant)] = find_length(variant, vts)
        #find max length / scale factor
        maxlen = max(variant_to_length.values())
        #scale by that length
        for variant in edge_variants:
            if variant_to_length[str(variant)] != maxlen:
                newpt = scale(variant, maxlen, vts, variant_to_length[str(variant)])
                vts[int(variant[1])-1] = newpt[1]
                vts[int(variant[0])-1] = newpt[0]
                
            
def find_length(variant, vts):
    pt0 = vts[int(variant[0])-1]
    pt1 = vts[int(variant[1])-1]
    
    #convert to floats
            
    pt0 = [float(x) for x in pt0]
    pt1 = [float(x) for x in pt1]
            
    #length = spatial.distance.cdist(pt0,pt1, "euclidean")
    length = euclidean_dist(pt0,pt1)
    return length

def scale(variant, factor, vts, currentlen):
    pt0 = vts[int(variant[0])-1]
    pt1 = vts[int(variant[1])-1]
            
    #convert to floats
            
    pt0 = [float(x) for x in pt0]
    pt1 = [float(x) for x in pt1]

    
    midpt = midpoint(pt0, pt1)

    newpt_x = pt0[0] + (pt1[0]-pt0[0]) / currentlen * factor
    newpt_y = pt0[1] + (pt1[1]-pt0[1]) / currentlen * factor

    newpt1 = [newpt_x,newpt_y]

    new_midpt = midpoint(pt0, newpt1)
    diff_x = new_midpt[0] - midpt[0]
    diff_y = new_midpt[1] - midpt[1]
    
    newpt1 = [newpt1[0]-diff_x, newpt1[1]-diff_y]

    newpt0 = [pt0[0]-diff_x, pt0[1]-diff_y]
    
    return [[str(round(x,4)) for x in newpt0], [str(round(x,4)) for x in newpt1]]

def midpoint(pt_a, pt_b):
    return [(pt_a[0]+pt_b[0])/2.0, (pt_a[1]+pt_b[1])/2.0]

def euclidean_dist(pt_a,pt_b):
    diff1 = pt_a[0] - pt_b[0]
    diff2 = pt_a[1] - pt_b[1]
    return math.sqrt(diff1*diff1 + diff2*diff2)
