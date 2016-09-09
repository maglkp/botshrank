#!/usr/bin/python

#
def nextMove(n,r,c,grid):
    return ""

n = int(input())
r, c = [int(i) for i in input().strip().split()]
grid = []
for i in range(0, n):
    grid.append(input())

print(nextMove(n,r,c,grid))


def nextMove(path):
    if path[0] < 0:
        print("UP")
    elif path[0] > 0:
        print("DOWN")
    elif path[1] < 0:
        print("LEFT")
    elif path[1] > 0:
        print("RIGHT")
    else:
        print("F*&%, already in the princess")


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
nextMove(path)
