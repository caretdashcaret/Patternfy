import math

class SeamEquilizer():

    def __init__(self, edges, vts):
        self.edges = edges
        self.vts = vts

    #makes sure seams are of equal length for reassembly
    def equilize(self):

        for edge_key, edge_variants in self.edges.items():

            variants_to_lengths = self.find_lengths_of_edge_variants(edge_variants)

            #find max length / scale factor
            max_edge_length = max(variants_to_lengths.values())

            #scale by that length
            self.scale_variant_edge(edge_variants, max_edge_length, variants_to_lengths)


    def find_lengths_of_edge_variants(self, edge_variants):
        variants_to_lengths = {}
        for variant in edge_variants:
            hashable_key = str(variant)
            variants_to_lengths[hashable_key] = self.find_length(variant)

        return variants_to_lengths

    def scale_variant_edge(self, edge_variants, scale_factor, variants_lengths):
        for variant in edge_variants:
            hashable_key = str(variant)
            if variants_lengths[hashable_key] != scale_factor:
                pt0, pt1 = self.get_vts_values(variant)
                newpt0, newpt1 = self.scale(pt0, pt1, scale_factor, variants_lengths[hashable_key])
                self.set_new_vts_values(newpt0, newpt1, variant)

    def set_new_vts_values(self, value_0, value_1, edge_variant):
        idx_0, idx_1 = self.get_vts_index_for_edge(edge_variant)
        self.vts[idx_0] = value_0
        self.vts[idx_1] = value_1

    def get_vts_index_for_edge(self, edge_variant):
        return edge_variant[0] - 1, edge_variant[1] - 1

    def get_vts_values(self, edge_variant):
        idx_0, idx_1 = self.get_vts_index_for_edge(edge_variant)
        return self.vts[idx_0], self.vts[idx_1]

    def find_length(self, edge_variant):
        pt0, pt1 = self.get_vts_values(edge_variant)

        length = self.euclidean_dist(pt0,pt1)
        return length

    def scale(self, pt0, pt1, factor, currentlen):

        midpt = self.midpoint(pt0, pt1)

        newpt_x = pt0[0] + (pt1[0]-pt0[0]) / currentlen * factor
        newpt_y = pt0[1] + (pt1[1]-pt0[1]) / currentlen * factor

        newpt1 = [newpt_x,newpt_y]

        new_midpt = self.midpoint(pt0, newpt1)
        diff_x = new_midpt[0] - midpt[0]
        diff_y = new_midpt[1] - midpt[1]

        newpt0 = [pt0[0]-diff_x, pt0[1]-diff_y]
        newpt1 = [newpt1[0]-diff_x, newpt1[1]-diff_y]

        return [round(x,4) for x in newpt0], [round(x,4) for x in newpt1]

    def midpoint(self, pt_a, pt_b):
        return [(pt_a[0]+pt_b[0])/2.0, (pt_a[1]+pt_b[1])/2.0]

    def euclidean_dist(self, pt_a, pt_b):
        diff1 = pt_a[0] - pt_b[0]
        diff2 = pt_a[1] - pt_b[1]
        return math.sqrt(diff1 * diff1 + diff2 * diff2)
