#!/usr/bin/python


def nextMoveOnPath(path):
    if path[0] < 0:
        return "UP"
    elif path[0] > 0:
        return "DOWN"
    elif path[1] < 0:
        return "LEFT"
    elif path[1] > 0:
        return "RIGHT"
    else:
        return "F*&%, already in the princess"


def nextMove(n, r, c, grid):
    grid = "".join(grid)
    # mario_ix = 0
    princess_ix = 0
    for i in range(0, n * n):
        if grid[i] == 'p':
            princess_ix = i
            # elif grid[i] == 'm':
            #    mario_ix = i

    # mario_pos = (int(mario_ix / n), mario_ix % n)
    mario_pos = (r, c)
    princess_pos = (int(princess_ix / n), princess_ix % n)

    path = (princess_pos[0] - mario_pos[0], princess_pos[1] - mario_pos[1])
    return nextMoveOnPath(path)


n = int(input())
r, c = [int(i) for i in input().strip().split()]
grid = []
for i in range(0, n):
    grid.append(input())

print(nextMove(n, r, c, grid))
