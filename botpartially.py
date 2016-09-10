#!/usr/bin/python
import os.path

N = 5
GRID_FILE = "grid.dat"


# prints next action
def go_to_nearest_fog():
    pass


def next_move(posx, posy, board):
    # if on dust CLEAN
    if board[posx][posy] == 'd':
        print("CLEAN")
        return

    board = retrieve_merge_grid(board)

    # go through all fields and find closest dust
    bot_pos = (posx, posy)
    next_dust = -1
    next_dust_dist = 10 * N
    for r in range(N):
        for c in range(N):
            if board[r][c] == 'd':
                dist = distance(bot_pos, (r, c))
                if dist < next_dust_dist:
                    next_dust_dist = dist
                    next_dust = (r, c)

    # if dust is visible go to closest dust
    if next_dust != -1:
        print(get_next_move(bot_pos, next_dust))
    else:
        print(go_to_nearest_fog())

    save_board(board)


def read_grid():
    if not os.path.isfile(GRID_FILE):
        return ['ooooo' for i in range(N)]
    return [line.strip() for line in open(GRID_FILE, 'r')]


def merge_grid(saved_grid, current_grid):
    for i in range(N):
        for j in range(N):
            if saved_grid[i][j] == 'd' or saved_grid[i][j] == '-':
                current_grid[i][j] = saved_grid[i][j]
    return current_grid


def save_board(board):
    grid_file = open(GRID_FILE, 'w')
    for line in board:
        grid_file.write("".join(line) + '\n')
    grid_file.close()


def retrieve_merge_grid(grid):
    return merge_grid(read_grid(), grid)


def get_next_move(bot_pos, next_dust):
    diff = (next_dust[0] - bot_pos[0], next_dust[1] - bot_pos[1])
    if diff[0] < 0:
        return "UP"
    elif diff[0] > 0:
        return "DOWN"
    elif diff[1] < 0:
        return "LEFT"
    elif diff[1] > 0:
        return "RIGHT"
    else:
        return "NOOP (f**k, already there, nothing to do, my meaning has ceased)"


def distance(bot, pos):
    return abs(bot[0] - pos[0]) + abs(bot[1] - pos[1])


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(N)]
    next_move(pos[0], pos[1], board)


