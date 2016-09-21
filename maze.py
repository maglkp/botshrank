#!/usr/bin/python
import os.path

GRID_FILE = "maze.dat"
NOT_FOUND = -1
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
EMPTY = '-'
FOG = 'o'
SURROUNDINGS_SIZE = 3
FACING_ERR = "Invalid facing"
HERO = 'b'


# reads and returns cached bot position, facing and grid as a 3-tuple
# if no cache file exists assume neutral (UP) initial facing, (1,1) and no grid is returned
def read_grid():
    if not os.path.isfile(GRID_FILE):
        return (1, 1), UP, NOT_FOUND

    f = open(GRID_FILE, 'r')
    contents = [line.strip() for line in f]
    pos = [int(i) for i in contents[0].strip().split()]
    facing = contents[1]
    grid = contents[2:]
    f.close()
    return pos, facing, grid


# rotates a 3x3 grid so that it's facing the conventional neutral UP
def normalize_grid(grid, facing):
    grid[1][1] = EMPTY
    if facing == UP:
        return grid
    if facing == DOWN:
        return rot_right(rot_right(grid))
    if facing == LEFT:
        return rot_right(rot_right(rot_right(grid)))
    if facing == RIGHT:
        return rot_right(grid)
    raise FACING_ERR


# rotates a 3x3 grid 90 degrees right, returns the rotated grid
def rot_right(grid):
    # 3x3 zeroes
    rot = [[0 for x in range(3)] for y in range(3)]
    rot[0][0] = grid[2][0]
    rot[1][0] = grid[2][1]
    rot[2][0] = grid[2][2]
    rot[0][2] = grid[0][0]
    rot[1][2] = grid[0][1]
    rot[2][2] = grid[0][2]
    rot[0][1] = grid[1][0]
    rot[1][1] = grid[1][1]
    rot[2][1] = grid[1][2]
    return rot


def expand_grid_on_edge(grid_map, pos):
    # max row value or length of any column
    max_r = len(grid_map)
    # max col value or length of any row
    max_c = len(grid_map[0])
    # bot position
    row = pos[0]
    col = pos[1]

    if row == 0:
        grid_map.insert(0, [FOG for i in range(max_c)])
        return grid_map, (pos[0] + 1, pos[1])
    if row == max_r:
        grid_map.append([FOG for i in range(max_c)])
        return grid_map, pos

    # if not on the edge of the current world map return the current structure
    return grid_map, pos


def next_move(surr):
    # read cached grid map, current bot position and its last move (facing)
    pos, facing, grid_map = read_grid()

    # normalize the current surroundings to match the grid map direction by rotating it
    surr = normalize_grid(surr, facing)

    # if there was no cached map there initialize it with the current surroundings
    if grid_map == NOT_FOUND:
        grid_map = surr

    # expand the map container if the bot is at the edge and update its position
    grid_map, pos = expand_grid_on_edge(grid_map, pos)




# translates move taken on global map to local surroundings defined by previous facing
# (bot sees what is in front of it as above it)
def translate_move_into_local_coord(facing, move):
    if facing == UP:
        return move
    if facing == RIGHT:
        return rotate_90_right(rotate_90_right(rotate_90_right(move)))
    if facing == LEFT:
        return rotate_90_right(move)
    if facing == DOWN:
        return rotate_90_right(rotate_90_right(move))
    raise FACING_ERR


# rotates a move 90 degrees RIGHT (UP becomes RIGHT etc.)
def rotate_90_right(move):
    if move == UP:
        return RIGHT
    if move == RIGHT:
        return DOWN
    if move == DOWN:
        return LEFT
    if move == LEFT:
        return UP
    raise FACING_ERR


if __name__ == "__main__":
    bot_num = input().strip()
    surroundings = [[j for j in input().strip()] for i in range(SURROUNDINGS_SIZE)]
    next_move(surroundings)
