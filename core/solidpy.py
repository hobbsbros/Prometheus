# Solidpy
# A super basic Python library for processing STL files

def to_dec(mantissa):
    split_num = mantissa.split("e")
    m = float(split_num[0])
    e = float(split_num[1])
    return m*pow(10, e)

def to_man(decimal):
    return "{:e}".format(decimal)

def mag(v):
    magnitude = 0
    for element in v:
        magnitude += pow(element, 2)
    return pow(magnitude, 0.5)

def normalize(v):
    m = mag(v)
    return (v[0]/m, v[1]/m, v[2]/m)

def cross_product(a, b):
    v = (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])
    return v

class Facet:
    def __init__(self, n):
        self.normal_vector = n
        self.vertices = []
        self.side_vectors = []
        self.perimeter = 0
        self.area = 0
    def add_vertex(self, v):
        self.vertices.append(v)
    def compute_side_vectors(self):
        v1, v2, v3 = self.vertices[0], self.vertices[1], self.vertices[2]
        s1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
        s2 = (v3[0] - v2[0], v3[1] - v2[1], v3[2] - v2[2])
        s3 = (v1[0] - v3[0], v1[1] - v3[1], v1[2] - v3[2])
        self.side_vectors = (s1, s2, s3)
        return self.side_vectors
    def compute_perimeter(self):
        self.compute_side_vectors()
        self.perimeter = 0
        for v in self.side_vectors:
            self.perimeter.append(mag(v))
        return self.perimeter
    def compute_area(self):
        self.compute_side_vectors()
        self.area = 0
        s1 = self.side_vectors[0]
        s2 = self.side_vectors[1]
        self.area = 0.5*mag(cross_product(s1, s2))
        return self.area

class Stl:
    def __init__(self, filename):
        self.file = open(filename, mode="r+")
        self.file_raw = self.file.read().split("\n")
        self.text = []
        # Prepare self.file for parsing
        for line in self.file_raw:
            a = line.strip().split(" ")
            b = []
            for value in a:
                if value != "":
                    b.append(value)
            self.text.append(b)
        self.stl = []
        self.surface_area = 0
        self.volume = 0
    def parse(self):
        self.stl = []
        for line in self.text:
            if line != []:
                command = line[0]
                if command == "facet":
                    # Create a new facet with a specified normal vector
                    try:
                        nx = to_dec(line[2])
                        ny = to_dec(line[3])
                        nz = to_dec(line[4])
                    except:
                        nx = float(line[2])
                        ny = float(line[3])
                        nz = float(line[4])
                    self.stl.append(Facet((nx, ny, nz)))
                elif command == "vertex":
                    # Add a vertex to the current facet
                    try:
                        vx = to_dec(line[1])
                        vy = to_dec(line[2])
                        vz = to_dec(line[3])
                    except:
                        vx = float(line[1])
                        vy = float(line[2])
                        vz = float(line[3])
                    self.stl[-1].add_vertex((vx, vy, vz))
    def compute_surface_area(self):
        # Approximate surface area by summing area of all facets
        self.surface_area = 0
        for facet in self.stl:
            self.surface_area += facet.compute_area()
        return self.surface_area
    def compute_volume(self):
        # Approximate buoyancy force on the object to approximate volume
        # This function is not exactly accurate; expect up to 1% error for complex geometries
        self.volume = 0
        buoyancy_vector = [0, 0, 0]
        for facet in self.stl:
            facet.compute_area()
            n = normalize(facet.normal_vector)
            a = facet.area
            depth = (facet.vertices[0][2] + facet.vertices[1][2] + facet.vertices[2][2])/3
            buoyancy_vector[0] += a*depth*n[0]
            buoyancy_vector[1] += a*depth*n[1]
            buoyancy_vector[2] += a*depth*n[2]
        return mag(buoyancy_vector)
    def initialize(self):
        # Clears the file and prepares for writing
        self.file.write("solid ASCII\n")
    def write_facet(self, n, v):
        # Write a facet using a normal vector and a tuple of vertex vectors
        v1, v2, v3 = v[0], v[1], v[2]
        n1, n2, n3 = to_man(n[0]), to_man(n[1]), to_man(n[2])
        self.file.write(f"facet normal {n1} {n2} {n3}\n")
        v11, v12, v13 = to_man(v1[0]), to_man(v1[1]), to_man(v1[2])
        v21, v22, v23 = to_man(v2[0]), to_man(v2[1]), to_man(v2[2])
        v31, v32, v33 = to_man(v3[0]), to_man(v3[1]), to_man(v3[2])
        self.file.write("outer loop\n")
        self.file.write(f"vertex {v11} {v12} {v13}\n")
        self.file.write(f"vertex {v21} {v22} {v23}\n")
        self.file.write(f"vertex {v31} {v32} {v33}\n")
        self.file.write("endloop\nendfacet\n")
    def finalize(self):
        # Closes the file
        self.file.write("endsolid")
        self.file.close()
