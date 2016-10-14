#!/usr/bin/python
import os.path
import copy

import sys

GRID_FILE_P1 = "maze_p1.dat"
GRID_FILE_P2 = "maze_p2.dat"
NOT_FOUND = -1
UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"
EMPTY = '-'
EXIT = 'e'
FOG = 'o'
VISITED = '^'
SURROUNDINGS_SIZE = 3
FACING_ERR = "Invalid facing"
ACTION_ERR = "Invalid action"
NO_PATH = "No path found"
HERO = 'b'


def print_grid(grid):
    for line in grid:
        for cell in line:
            sys.stdout.write(cell)
        sys.stdout.write("\n")
    sys.stdout.write("\n")


# reads and returns cached bot position, facing and grid as a 3-tuple
# if no cache file exists assume neutral (UP) initial facing, (1,1) and no grid is returned
def read_grid(bot_num):

    grid_file = (GRID_FILE_P1 if bot_num == 1 else GRID_FILE_P2)

    if not os.path.isfile(grid_file):
        return (1, 1), UP, NOT_FOUND

    f = open(grid_file, 'r')
    contents = [line.strip() for line in f]
    pos = [int(i) for i in contents[0].strip().split()]
    facing = contents[1]
    grid = [[j for j in line.strip()] for line in contents[2:]]
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


# adds extra row or column - not both as the rules of the prevent it with no cross moves
# and preventing bot from entering the world edge.
# TODO test this thing again
def expand_grid_when_bot_on_edge(grid_map, pos):
    # max row value or length of any column
    max_r = len(grid_map) - 1
    # max col value or length of any row
    max_c = len(grid_map[0]) - 1
    # bot position
    row = pos[0]
    col = pos[1]

    # add row above map
    if row == 0:
        grid_map.insert(0, [FOG for _ in range(max_c + 1)])
        return grid_map, (pos[0] + 1, pos[1])
    # add row below map
    if row == max_r:
        grid_map.append([FOG for _ in range(max_c + 1)])
        return grid_map, pos
    # add col on the left
    if col == 0:
        grid_map = [[FOG] + r for r in grid_map]
        return grid_map, (pos[0], pos[1] + 1)
    # add col on the right
    if col == max_c:
        grid_map = [r + [FOG] for r in grid_map]
        return grid_map, pos

    # if not on the edge of the current world map return the current structure
    return grid_map, pos


# adds currently available surroundings to the global map
def add_surroundings_to_grid(grid_map, surr, pos):
    x = pos[0]
    y = pos[1]
    # copy 8 neighbouring cells manually
    grid_map[x - 1][y - 1] = surr[0][0]
    grid_map[x - 1][y] = surr[0][1]
    grid_map[x - 1][y + 1] = surr[0][2]
    grid_map[x][y - 1] = surr[1][0]
    grid_map[x][y + 1] = surr[1][2]
    grid_map[x + 1][y - 1] = surr[2][0]
    grid_map[x + 1][y] = surr[2][1]
    grid_map[x + 1][y + 1] = surr[2][2]
    return grid_map


def exit_nearby(grid_map, bot_pos):
    x = bot_pos[0]
    y = bot_pos[1]
    return grid_map[x][y - 1] == EXIT or \
           grid_map[x][y + 1] == EXIT or \
           grid_map[x - 1][y] == EXIT or \
           grid_map[x + 1][y] == EXIT


# finds nearest grid
def find_next_target(grid_map, bot_pos):
    search_grid = copy.deepcopy(grid_map)
    path = visit(search_grid, bot_pos, [])

    if len(path) == 0:
        raise NO_PATH

    # return first cell on the path to chosen target
    return path[0]


def visit(search_grid, cell, path):
    neighbours = get_unvisited_neighbours(search_grid, cell)
    search_grid[cell[0]][cell[1]] = VISITED

    for nb in neighbours:
        if is_destination_candidate(search_grid, nb):
            return path + [nb]
        val = visit(search_grid, nb, path + [nb])
        if val != NOT_FOUND:
            return val
    return NOT_FOUND


def get_unvisited_neighbours(search_grid, pos):
    unvisited_neighbours = []
    if is_unvisited(search_grid, pos[0] - 1, pos[1]):
        unvisited_neighbours.append((pos[0] - 1, pos[1]))
    if is_unvisited(search_grid, pos[0] + 1, pos[1]):
        unvisited_neighbours.append((pos[0] + 1, pos[1]))
    if is_unvisited(search_grid, pos[0], pos[1] - 1):
        unvisited_neighbours.append((pos[0], pos[1] - 1))
    if is_unvisited(search_grid, pos[0], pos[1] + 1):
        unvisited_neighbours.append((pos[0], pos[1] + 1))
    return unvisited_neighbours


def is_unvisited(search_grid, posr, posc):
    # max row value or length of any column
    max_r = len(search_grid) - 1
    # max col value or length of any row
    max_c = len(search_grid[0]) - 1
    out_of_bounds = posr < 0 or posc < 0 or posr > max_r or posc > max_c
    return not out_of_bounds and (search_grid[posr][posc] == EMPTY or search_grid[posr][posc] == FOG)


# returns true if a position is at the map boundary
def is_destination_candidate(search_grid, pos):
    # max row value or length of any column
    max_r = len(search_grid) - 1
    # max col value or length of any row
    max_c = len(search_grid[0]) - 1
    return pos[0] == 0 or pos[1] == 0 or pos[0] == max_r or pos[1] == max_c


def go_to_exit(grid_map, bot_pos):
    x = bot_pos(0)
    y = bot_pos(1)

    if grid_map[x][y - 1] == EXIT:
        return LEFT
    if grid_map[x][y + 1] == EXIT:
        return RIGHT
    if grid_map[x - 1][y] == EXIT:
        return UP
    if grid_map[x + 1][y] == EXIT:
        return DOWN
    raise ACTION_ERR


# takes current bot position and a neighbouring cell and outputs an action
# to move the bot to that cell
def get_move_to_neighbour(neighbour, bot_pos):
    dr = neighbour[0] - bot_pos[0]
    dc = neighbour[1] - bot_pos[1]
    if dr == 1:
        return DOWN
    if dr == -1:
        return UP
    if dc == 1:
        return RIGHT
    if dc == 1:
        return LEFT


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


def save_board(board, bot_pos, facing, bot_num):

    grid_file = (GRID_FILE_P1 if bot_num == 1 else GRID_FILE_P2)
    f = open(grid_file, 'w')

    f.write(str(bot_pos[0]) + " " + str(bot_pos[1]) + '\n')
    f.write(facing + '\n')
    for line in board:
        f.write("".join(line) + '\n')
    f.close()


# updates bot position by 1 cell based on current position and current action
def update_bot_pos(bot_pos, current_action):
    if current_action == UP:
        return bot_pos[0] - 1, bot_pos[1]
    if current_action == RIGHT:
        return bot_pos[0], bot_pos[1] + 1
    if current_action == DOWN:
        return bot_pos[0] + 1, bot_pos[1]
    if current_action == LEFT:
        return bot_pos[0], bot_pos[1] - 1
    raise FACING_ERR


def next_move(surr, bot_num):
    # read cached grid map, current bot position and its last move (facing)
    bot_pos, facing, grid_map = read_grid(bot_num)

    # normalize the current surroundings to match the grid map direction by rotating it
    surr = normalize_grid(surr, facing)

    # if there was no cached map there initialize it with the current surroundings
    if grid_map == NOT_FOUND:
        grid_map = surr

    # expand the map container if the bot is at the edge and update its position
    grid_map, bot_pos = expand_grid_when_bot_on_edge(grid_map, bot_pos)

    # add current bot's surroundings
    grid_map = add_surroundings_to_grid(grid_map, surr, bot_pos)

    if exit_nearby(grid_map, bot_pos):
        current_action = go_to_exit(grid_map, bot_pos)
    else:
        current_action = get_move_to_neighbour(find_next_target(grid_map, bot_pos), bot_pos)

    bot_pos = update_bot_pos(bot_pos, current_action)

    # save env to file
    # new_bot_pos, this_move_global_coord, grid
    save_board(grid_map, bot_pos, current_action, bot_num)

    # translate action to local (original) coordinates
    move_into_local_coord = translate_move_into_local_coord(facing, current_action)
    return move_into_local_coord


def read_grid_from_file(path):
    f = open(path, 'r')
    contents = [line.strip() for line in f]
    grid = [[j for j in line.strip()] for line in contents]
    f.close()
    return grid


def test_visit():
    grid = read_grid_from_file("visit_input01.txt")
    bot_pos = (2, 2)
    print(visit(grid, bot_pos, []))


if __name__ == "__main__":
    bot_num = int(input().strip())
    surroundings = [[j for j in input().strip()] for i in range(SURROUNDINGS_SIZE)]
    print(next_move(surroundings, bot_num))
