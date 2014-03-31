class ObjectLoader():
    """handles reading of the OBJ files"""

    def __init__(self, filename):
        self.filename = filename

    def load_obj(self):
        """vts are the texture coordinates (x,y)
        faces are an array of points, indexing into the vts"""
        vts, faces = self.read_obj_file()

        f_to_vts = self.map_faces_to_vts(faces)

        edges_to_vts = self.map_edges_to_vts(faces)

        return f_to_vts, edges_to_vts, vts

    def read_obj_file(self):
        """extracts the texture coordinates, vts, an array of coordinates
        and faces, a array of points that index into the vts array, as well as other arrays"""

        obj_file = open(self.filename)
        #texture coords
        vts = []

        faces = []

        for line in obj_file:
            if line.startswith("vt"):
                vts.append(self.parse_coordinates(line))
            if line.startswith("f"):
                faces.append(self.parse_face(line))

        return vts, faces

    def map_edges_to_vts(self, faces):
        edges_to_vts = {}
        for face_idx, face_value in enumerate(faces):
            edges_to_vts = self.parse_edges(face_value, edges_to_vts)
        return edges_to_vts

    def parse_edges(self, points_array, edges_to_vts):
        max_edges = len(points_array)

        this_edge = 0
        next_edge = 1
        while this_edge < max_edges:
            start = points_array[this_edge]
            end = points_array[next_edge]
            edge = (start[0], end[0])
            edge2 = (end[0],start[0])

            if edge in edges_to_vts:
                edges_to_vts[edge].append([start[1],end[1]])
            elif edge2 in edges_to_vts:
                edges_to_vts[edge2].append([end[1], start[1]])
            else:
                edges_to_vts[edge] = [[start[1],end[1]]]

            #increase count
            this_edge += 1
            if next_edge == max_edges - 1:
                next_edge = 0
            else:
                next_edge += 1

        return edges_to_vts

    def parse_coordinates(self, line):
        coords = line.split()
        return [float(x) for x in coords[1:3]]

    def parse_face(self, line):
        parsed_face = []
        points_in_face = line.split()
        for point in points_in_face[1:]:
            split_point = point.split("/")
            converted_to_int = [int(x) for x in split_point]
            parsed_face.append(converted_to_int)
        return parsed_face

    def extract_vt_index(self, point_array):
        extracted_vts = []
        for point in point_array:
            extracted_vts.append(point[1])
        return extracted_vts

    def map_faces_to_vts(self, faces):
        f_to_vts = {}
        for face_idx, face_value in enumerate(faces):
            f_to_vts[face_idx] = self.extract_vt_index(face_value)
        return f_to_vts