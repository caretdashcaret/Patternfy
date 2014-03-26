import math

#makes sure seams are of equal length for reassembly
def seam_equilize(edges, vts):
    for edge_key, edge_variants in edges.items():        
        
        variants_to_lengths = find_lengths_of_edge_variants(edge_variants, vts)
        
        #find max length / scale factor
        max_edge_length = max(variants_to_lengths.values())
        
        #scale by that length
        scale_variant_edge(edge_variants, max_edge_length, variants_to_lengths, vts)
        

def find_lengths_of_edge_variants(edge_variants, vts):    
    variants_to_lengths = {}
    for variant in edge_variants:
        hashable_key = str(variant)
        variants_to_lengths[hashable_key] = find_length(variant, vts)
               
    return variants_to_lengths

def scale_variant_edge(edge_variants, scale_factor, variants_lengths, vts):
    for variant in edge_variants:
        hashable_key = str(variant)
        if variants_lengths[hashable_key] != scale_factor:
            newpt0, newpt1 = scale(variant, scale_factor, vts, variants_lengths[hashable_key])
            set_new_edge_points(newpt1, newpt0, variant, vts)

def set_new_edge_points(value_1, value_0, edge_variant, vts):
    idx_1, idx_0 = vts_index_for_edge(edge_variant)
    vts[idx_1] = value_1
    vts[idx_0] = value_0

def vts_index_for_edge(edge_variant):
    return edge_variant[1] - 1, edge_variant[0] - 1

def get_vts_values(edge_variant, vts):
    idx_1, idx_0 = vts_index_for_edge(edge_variant)
    return vts[idx_1], vts[idx_0]
            
def find_length(edge_variant, vts):
    pt1, pt0 = get_vts_values(edge_variant, vts)
    
    length = euclidean_dist(pt0,pt1)
    return length

def scale(variant, factor, vts, currentlen):
    
    pt1, pt0 = get_vts_values(variant, vts)

    midpt = midpoint(pt0, pt1)

    newpt_x = pt0[0] + (pt1[0]-pt0[0]) / currentlen * factor
    newpt_y = pt0[1] + (pt1[1]-pt0[1]) / currentlen * factor

    newpt1 = [newpt_x,newpt_y]

    new_midpt = midpoint(pt0, newpt1)
    diff_x = new_midpt[0] - midpt[0]
    diff_y = new_midpt[1] - midpt[1]
    
    newpt1 = [newpt1[0]-diff_x, newpt1[1]-diff_y]

    newpt0 = [pt0[0]-diff_x, pt0[1]-diff_y]
    
    return [round(x,4) for x in newpt0], [round(x,4) for x in newpt1]

def midpoint(pt_a, pt_b):
    return [(pt_a[0]+pt_b[0])/2.0, (pt_a[1]+pt_b[1])/2.0]

def euclidean_dist(pt_a, pt_b):
    diff1 = pt_a[0] - pt_b[0]
    diff2 = pt_a[1] - pt_b[1]
    return math.sqrt(diff1 * diff1 + diff2 * diff2)
