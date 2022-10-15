import math
r = open("find.in", "r")
w = open("find.out", "w")
lines = r.readlines()
N, M, Dx, Dy, K = int(lines[0].split()[0]), int(lines[0].split()[1]), float(lines[0].split()[2]), float(lines[0].split()[3]), int(lines[0].split()[4])

coordinates = []
for n in range(K):
    coordinates.append([float(lines[n+1].split()[0]), float(lines[n+1].split()[1])])
# print(N, M, Dx, Dy, K)
for coordinate in coordinates:
    if coordinate[0] % Dx == Dx/2:
        coordinate[0] = int(coordinate[0]/Dx - 0.5)
    else:
        coordinate[0] = round(coordinate[0]/Dx)
        if coordinate[0]*Dx >= (N-1)*Dx:
            coordinate[0] = N-1
    if coordinate[1] % Dy == Dy/2:
        coordinate[1] = int(coordinate[1]/Dy - 0.5)
    else:
        coordinate[1] = round(coordinate[1]/Dy)
        if coordinate[1]*Dy >= (M-1)*Dy:
            coordinate[1] = M-1
    print(coordinate[0], coordinate[1], file=w)

