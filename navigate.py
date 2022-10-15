from shapely.geometry import Polygon, Point
r = open("navigate.in", "r")
w = open("navigate.out", "w")
lines = r.readlines()
N, M, K, P = int(lines[0].split()[0]), int(lines[0].split()[1]), int(lines[0].split()[2]), int(lines[0].split()[3])
waypoints = []
polygons = []
polygons2 = []
start = K+1
num = 0


def points_within(poly):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    for a in range(int(min_x), int(max_x + 1)):
        for b in range(int(min_y), int(max_y + 1)):
            if Point([a, b]).within(poly):
                points.append([a, b])
    return points
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def findpath(grid, start, end):

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []


    open_list.append(start_node)
    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for movement in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: #include diagonals

            node_position = (current_node.position[0] + movement[0], current_node.position[1] + movement[1])

            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (len(grid[len(grid)-1]) -1) or node_position[1] < 0:
                continue

            if grid[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


for n in range(K):
    waypoints.append([int(lines[n+1].split()[0]), int(lines[n+1].split()[1])])
while 1: #find coordinates of points ON the polygon and INSIDE the polygon since that matters for the pathfinding algo
    for index in range(start+1, start+1+int(lines[start])):
        polygons2.append([int(lines[index].split()[0]), int(lines[index].split()[1])])
        polygons.append([int(lines[index].split()[0]), int(lines[index].split()[1])])
    for index in range(start+1, start+int(lines[start])):
        aftx = int(lines[index+1].split()[0])
        afty = int(lines[index+1].split()[1])
        befx = int(lines[index].split()[0])
        befy = int(lines[index].split()[1])
        if abs(aftx-befx) > 1:
            if afty==befy:
                if aftx>befx:
                    for x in range(befx+1, aftx):
                        polygons.append([x, afty])
                else:
                    for x in range(aftx+1, befx):
                        polygons.append([x, afty])
            else:
                if aftx>befx and afty>befy:
                    for x in range(befx+1, aftx):
                        polygons.append([x, befy+x-befx])
                elif aftx>befx:
                    for x in range(befx+1, aftx):
                        polygons.append([x, befy-(x-befx)])
                elif afty>befy:
                    for x in range(aftx+1, befx):
                        polygons.append([x, afty-(x-aftx)])
                else:
                    for x in range(aftx+1, befx):
                        polygons.append([x, afty+(x-aftx)])
        elif abs(afty-befy) > 1:
            if afty>befy:
                for y in range(befy+1, afty):
                    polygons.append([befx, y])
            else:
                for y in range(afty+1, befy):
                    polygons.append([befx, y])

    coords = [(n[0], n[1]) for n in polygons2]
    poly = Polygon(coords)
    for n in points_within(poly):
        polygons.append(n)

    start = start+1+int(lines[start])
    if num == P-1:
        break
    num += 1
    polygons2 = []
print(polygons)
grid = [[0]*N for _ in range(M)]

for obstacle in polygons:
    grid[N-obstacle[1]][obstacle[0]-1] = 1




for n in range(len(waypoints)-1):
    startx, starty, endx, endy = waypoints[n][0], waypoints[n][1], waypoints[n+1][0], waypoints[n+1][1]
    start, end = (M - starty, startx - 1), (M - endy, endx - 1)
    path = findpath(grid, start, end)
    for coord in path[0:len(path)-1]:
        x, y = coord[0], coord[1]

        # print([y + 1, M - x])
        print(y+1, M-x, file=w)
print(waypoints[len(waypoints)-1][0], waypoints[len(waypoints)-1][1], file=w)

