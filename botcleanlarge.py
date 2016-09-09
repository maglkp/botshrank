#!/usr/bin/python

# NxM board


def print_next_move(bot_pos, next_dust):
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
        return "NOOP"


def next_move(posx, posy, dimx, dimy, board):
    # def next_move(posr, posc, board):

    N = dimx
    M = dimy
    # if bot at dust CLEAN now
    if board[posx][posy] == 'd':
        print("CLEAN")
        return

    # go through all fields and find closest dust
    bot_pos = (posx, posy)
    next_dust = bot_pos
    next_dust_dist = 10 * (N + M)
    for r in range(N):
        for c in range(M):
            if board[r][c] == 'd':
                dist = distance(bot_pos, (r, c))
                if dist < next_dust_dist:
                    next_dust_dist = dist
                    next_dust = (r, c)

    # go to closest dust
    print(print_next_move(bot_pos, next_dust))


def distance(bot, pos):
    return abs(bot[0] - pos[0]) + abs(bot[1] - pos[1])


if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    dim = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(dim[0])]
    next_move(pos[0], pos[1], dim[0], dim[1], board)
