#!/usr/bin/python


def display_path_to_princess(path):
    if path[0] < 0:
        for x in range(0, -path[0]):
            print("UP")
    else:
        for x in range(0, path[0]):
            print("DOWN")

    if path[1] < 0:
        for x in range(0, -path[1]):
            print("LEFT")
    else:
        for x in range(0, path[1]):
            print("RIGHT")


m = int(input())
grid = []
for i in range(0, m):
    grid.append(input().strip())

grid = "".join(grid)
mario_ix = 0
princess_ix = 0
for i in range(0, m * m):
    if grid[i] == 'p':
        princess_ix = i
    elif grid[i] == 'm':
        mario_ix = i

mario_pos = (int(mario_ix / m), mario_ix % m)
princess_pos = (int(princess_ix / m), princess_ix % m)

path = (princess_pos[0] - mario_pos[0], princess_pos[1] - mario_pos[1])
display_path_to_princess(path)
