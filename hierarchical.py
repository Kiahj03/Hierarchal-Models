#Kiah Johnson
#CS 536

import sys
import math

def rotation_z(angle):
    radians = math.radians(angle)
    return [
        [math.cos(radians), -math.sin(radians), 0, 0],
        [math.sin(radians), math.cos(radians), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def rotation_y(angle):
    radians = math.radians(angle)
    return [
        [math.cos(radians), 0, math.sin(radians), 0],
        [0, 1, 0, 0],
        [-math.sin(radians), 0, math.cos(radians), 0],
        [0, 0, 0, 1]
    ]

def translation_z(z):
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ]

def transformation(m1, m2):
    res = [[0 for _ in range(4)] for _ in range(4)]
    for k in range(4):
        for j in range(4):
            res[k][j] = sum(m1[k][kj] * m2[kj][j] for kj in range(4))
    return res

def create_vertices(vertices, matrix):
    new_vertices = []
    for vt in vertices:
        x, y, z = vt
        new_x = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z + matrix[0][3]
        new_y = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z + matrix[1][3]
        new_z = matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z + matrix[2][3]
        new_vertices.append([new_x, new_y, new_z])
    return new_vertices

def cuboid_vertices(link):
    return [
        [-0.5, -0.5, 0],
        [0.5, -0.5, 0],
        [0.5, 0.5, 0],
        [-0.5, 0.5, 0],
        [-0.5, -0.5, link],
        [0.5, -0.5, link],
        [0.5, 0.5, link],
        [-0.5, 0.5, link]
    ]

def cuboid(vertices, index):
    print("Separator {")
    print("Coordinate3 {")
    print("point [")
    for v in vertices:
        print(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f},")
    print("]")
    print("}")
    print("IndexedLineSet {")
    print("coordIndex [")
    for idx in index:
        print(f"{idx[0]}, {idx[1]}, {idx[2]}, {idx[3]}, {idx[4]},")
    print("]")
    print("}")
    print("}")

def spheres(translation):
    print("Separator {")
    print("LightModel { model PHONG }")
    print("Material { diffuseColor 1.0 1.0 1.0 }")
    print("Transform { translation 0.000000 0.000000 0.000000 }")
    print("Sphere { radius 0.20 }")
    print("}")
    print("Separator {")
    print("LightModel { model PHONG }")
    print("Material { diffuseColor 1.0 1.0 1.0 }")
    print("Transform {")
    print(f"translation {translation[0]:.6f} {translation[1]:.6f} {translation[2]:.6f}")
    print("}")
    print("Sphere { radius 0.20 }")
    print("}")

def main():
    theta1 = -51 #t
    theta2 = 39 #u
    theta3 = 65 #v
    link1 = 4 #l
    link2 = 3 #m
    link3 = 2.5 #n

    args = sys.argv[1:]
    for kj in range(len(args)):
        if args[kj] == "-t":
            theta1 = float(args[kj + 1])
        elif args[kj] == "-u":
            theta2 = float(args[kj + 1])
        elif args[kj] == "-v":
            theta3 = float(args[kj + 1])
        elif args[kj] == "-l":
            link1 = float(args[kj + 1])
        elif args[kj] == "-m":
            link2 = float(args[kj + 1])
        elif args[kj] == "-n":
            link3 = float(args[kj + 1])

    base_vertices = [
        [-2, -2, 0],
        [2, -2, 0],
        [2, 2, 0],
        [-2, 2, 0],
        [-2, -2, 1],
        [2, -2, 1],
        [2, 2, 1],
        [-2, 2, 1]
    ]

    base_index = [
        [0, 1, 2, 0, -1],
        [0, 2, 3, 0, -1],
        [7, 6, 5, 7, -1],
        [7, 5, 4, 7, -1],
        [0, 3, 7, 0, -1],
        [0, 7, 4, 0, -1],
        [1, 5, 6, 1, -1],
        [1, 6, 2, 1, -1],
        [0, 4, 5, 0, -1],
        [0, 5, 1, 0, -1],
        [3, 2, 6, 3, -1],
        [3, 6, 7, 3, -1]
    ]
    print("#Inventor V2.0 ascii\n")
    cuboid(base_vertices, base_index)

    matrix = transformation(translation_z(1), rotation_z(theta1))
    link1_verts = create_vertices(cuboid_vertices(link1), matrix)
    cuboid(link1_verts, base_index)

    matrix = transformation(matrix, translation_z(link1))
    matrix = transformation(matrix, rotation_y(theta2))
    link2_verts = create_vertices(cuboid_vertices(link2), matrix)
    cuboid(link2_verts, base_index)

    matrix = transformation(matrix, translation_z(link2))
    matrix = transformation(matrix, rotation_y(theta3))
    link3_verts = create_vertices(cuboid_vertices(link3), matrix)
    cuboid(link3_verts, base_index)

    matrix = transformation(matrix, translation_z(link3))

    spheres([matrix[0][3], matrix[1][3], matrix[2][3]])

if __name__ == "__main__":
    main() 
