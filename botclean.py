#!/usr/bin/python

# 5x5 board
N = 5


# Head ends here
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
        return "NOOP (f**k, already there, nothing to do, my meaning has ceased)"


def next_move(posr, posc, board):
    # if bot at dust CLEAN now
    if board[posr][posc] == 'd':
        print("CLEAN")
        return

    # go through all fields and find closest dust
    bot_pos = (posr, posc)
    next_dust = bot_pos
    next_dust_dist = 10 * N
    for r in range(N):
        for c in range(N):
            if board[r][c] == 'd':
                dist = distance(bot_pos, (r, c))
                if dist < next_dust_dist:
                    next_dust_dist = dist
                    next_dust = (r, c)

    # go to closest dust
    print(print_next_move(bot_pos, next_dust))


def distance(bot, pos):
    return abs(bot[0] - pos[0]) + abs(bot[1] - pos[1])

# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(N)]
    next_move(pos[0], pos[1], board)
