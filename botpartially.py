#!/usr/bin/python3
import os.path


GRID_FILE = "grid.dat"

def next_move(posx, posy, board):
    print("")


def read_grid():
    if not os.path.isfile(GRID_FILE):
        return
    return []

if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(5)]
    next_move(pos[0], pos[1], board)


