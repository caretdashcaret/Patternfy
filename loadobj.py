from PIL import Image

##reads an obj file
def load_obj(filename):
    #open obj file
    obj_file = open(filename)

    #vertexes
    v = []
    
    #texture coords
    vt = []

    #faces
    f = []
    

    #face to texture coords
    f_to_vts = {}

    #edges to texture coords
    edges_to_vts = {}

    
    for line in obj_file:
        if line.startswith("v "):
            coords = line.split()
            v.append(coords[1:])
        if line.startswith("vt"):
            coords = line.split()
            vt.append(coords[1:3])
        if line.startswith("f"):
            coords = line.split()
            f.append(coords[1:])   

    
    numfaces = len(f)
    index = 0
    while index < numfaces:
        #face vts
        face = f[index]
        face_vts = []
        for point in face:
            processed_point = point.split("/")
            face_vts.append(processed_point[1])
        f_to_vts[index] = face_vts

        #edge vts
        this_edge = 0
        next_edge = 1
        edges = len(face)
        while this_edge < edges:
            start = face[this_edge].split("/")
            end = face[next_edge].split("/")
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
            if next_edge == edges-1:
                next_edge = 0
            else:
                next_edge += 1
            
        index += 1

    return [f_to_vts, edges_to_vts, vt]

