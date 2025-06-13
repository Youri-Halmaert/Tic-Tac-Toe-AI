#  --------------------------------
# |  0  1  2 | 9  10 11 | 18 19 20 |
# |  3  4  5 | 12 13 14 | 21 22 23 |
# |  6  7  8 | 15 16 17 | 24 25 26 |
#  --------------------------------
# | 27 28 29 | 36 37 38 | 45 46 47 |
# | 30 31 32 | 39 40 41 | 48 49 50 |
# | 33 34 35 | 42 43 44 | 51 52 53 |
#  --------------------------------
# | 54 55 56 | 63 64 65 | 72 73 74 |
# | 57 58 59 | 66 67 68 | 75 76 77 |
# | 60 61 62 | 69 70 71 | 78 79 80 |
#  --------------------------------


from math import inf
from collections import Counter
import itertools
from time import time

box_won = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
possible_goals = [(0, 4, 8), (2, 4, 6), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 1, 2), (3, 4, 5), (6, 7, 8)]


def translate(n):
    col = 3 * ((n // 9) % 3) + n % 3
    raw = 3 * ((n // 9) // 3) + (n % 9) // 3
    return raw, col


#def translate_other_side(raw, col):
#    return ((raw // 3) * 27) + ((raw % 3) * 3) + ((col // 3) * 9) + (col % 3)


'''def translate_state_other_side(statetable):
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c6 = []
    c7 = []
    c8 = []
    c9 = []

    for i in range(3):
        for j in range(9):
            if j < 3:
                c1.append(int(statetable[j][i]))
            if 2 < j and j < 6:
                c2.append(int(statetable[j][i]))
            if j > 5:
                c3.append(int(statetable[j][i]))

    for i in range(3, 6):
        for j in range(9):
            if j < 3:
                c4.append(int(statetable[j][i]))
            if 2 < j and j < 6:
                c5.append(int(statetable[j][i]))
            if j > 5:
                c6.append(int(statetable[j][i]))

    for i in range(6, 9):
        for j in range(9):
            if j < 3:
                c7.append(int(statetable[j][i]))
            if 2 < j and j < 6:
                c8.append(int(statetable[j][i]))
            if j > 5:
                c9.append(int(statetable[j][i]))
    state = [c1, c2, c3, c4, c5, c6, c7, c8, c9]
    state2 = []
    for i in range(9):
        for j in range(9):
            state2.append(state[i][j])
    state2 = "".join([str(_) for _ in state2])
    return state2'''


#def translate_state(state):
#    # faire devenir state en tableau
#    statetable = []
#    for i in range(3):
##        col = [int(state[i]), int(state[i + 3]), int(state[i + 6]), int(state[i + 27]), int(state[i + 27 + 3]),
#               int(state[i + 27 + 6]), int(state[i + 54]), int(state[i + 54 + 3]), int(state[i + 54 + 6])]
#        statetable.append(col)
#    for i in range(9, 12):
#        col = [int(state[i]), int(state[i + 3]), int(state[i + 6]), int(state[i + 27]), int(state[i + 27 + 3]),
#               int(state[i + 27 + 6]), int(state[i + 54]), int(state[i + 54 + 3]), int(state[i + 54 + 6])]
#        statetable.append(col)
#    for i in range(18, 21):
#        col = [int(state[i]), int(state[i + 3]), int(state[i + 6]), int(state[i + 27]), int(state[i + 27 + 3]),
#               int(state[i + 27 + 6]), int(state[i + 54]), int(state[i + 54 + 3]), int(state[i + 54 + 6])]
#        statetable.append(col)
#    return statetable


#def get_coordinates(row, col, grid_size=750, num_cells=9):
#    cell_size = grid_size / num_cells

#    center_x = col * cell_size + (cell_size / 2)
#    center_y = row * cell_size + (cell_size / 2)

#    return int(center_x), int(center_y)


def index(x, y):
    # converts raw and columns to the linear index above
    x -= 1
    y -= 1
    return ((x // 3) * 27) + ((x % 3) * 3) + ((y // 3) * 9) + (y % 3)


#def box(x, y):
#    # returns the box in which the move belongs to
#    return index(x, y) // 9


def next_box(i):
    # returns the nex box to play
    return i % 9


def indices_of_box(b):
    # returns a list that represent all positions within a specific 3x3 box in the overall 9x9 grid.
    return list(range(b * 9, b * 9 + 9))


#def print_board(state):  # to be able to play, but will be useless when the bot is incorporated to the game
#    for row in range(1, 10):
#        row_str = ["|"]
#        for col in range(1, 10):
#            row_str += [state[index(row, col)]]
#            if (col) % 3 == 0:
#                row_str += ["|"]
#        if (row - 1) % 3 == 0:
#            print("-" * (len(row_str) * 2 - 1))
#        print(" ".join(row_str))
#    print("-" * (len(row_str) * 2 - 1))


def add_piece(state, move, player):
    # returns the updated game
    if not isinstance(move, int):
        move = index(move[0], move[1])
    return state[: move] + player + state[move + 1:]


def update_box_won(state):
    # returns a list of won boxes
    temp_box_win = ["0"] * 9
    for b in range(9):
        idxs_box = indices_of_box(b)
        box_str = state[idxs_box[0]: idxs_box[-1] + 1]
        temp_box_win[b] = check_small_box(box_str)
    return temp_box_win


def check_small_box(box_str):
    # check if there is a winner in a small box
    global possible_goals
    for idxs in possible_goals:
        (x, y, z) = idxs
        if (box_str[x] == box_str[y] == box_str[z]) and box_str[x] != "0":
            return box_str[x]
    return "0"


def possible_moves(last_move):
    # returns a list of possible moves
    global box_won
    if not isinstance(last_move, int):
        last_move = index(last_move[0], last_move[1])
    box_to_play = next_box(last_move)
    idxs = indices_of_box(box_to_play)
    if box_won[box_to_play] != "0":
        pi_2d = [indices_of_box(b) for b in range(9) if box_won[b] == "0"]
        possible_indices = list(itertools.chain.from_iterable(pi_2d))
    else:
        possible_indices = idxs
    return possible_indices


def successors(state, player, last_move):
    # give all possible states of the specified state and player to play
    succ = []
    moves_idx = []
    possible_indexes = possible_moves(last_move)
    for idx in possible_indexes:
        if state[idx] == "0":
            moves_idx.append(idx)
            succ.append(add_piece(state, idx, player))
    return zip(succ, moves_idx)


#def print_successors(state, player, last_move):
#    for st in successors(state, player, last_move):
#        print_board(st[0])


def opponent(p):
    return "2" if p == "1" else "1"


def evaluate_small_box(box_str, player):
    # evaluate the heuristic value for small boxes
    global possible_goals
    score = 0
    three = Counter(player * 3)
    two = Counter(player * 2 + "0")
    one = Counter(player * 1 + "0" * 2)
    three_opponent = Counter(opponent(player) * 3)
    two_opponent = Counter(opponent(player) * 2 + "0")
    one_opponent = Counter(opponent(player) * 1 + "0" * 2)

    for idxs in possible_goals:
        (x, y, z) = idxs
        current = Counter([box_str[x], box_str[y], box_str[z]])

        if current == three:
            score += 100
        elif current == two:
            score += 10
        elif current == one:
            score += 1
        elif current == three_opponent:
            score -= 100
        elif current == two_opponent:
            score -= 10
        elif current == one_opponent:
            score -= 1
    return score


def evaluate_big_box(box_str, player):
    # evaluate the heuristic value for small boxes
    global possible_goals
    score = 0
    three = Counter(player * 3)
    two = Counter(player * 2 + "0")
    one = Counter(player * 1 + "0" * 2)
    three_opponent = Counter(opponent(player) * 3)
    two_opponent = Counter(opponent(player) * 2 + "0")
    one_opponent = Counter(opponent(player) * 1 + "0" * 2)

    for idxs in possible_goals:
        (x, y, z) = idxs
        current = Counter([box_str[x], box_str[y], box_str[z]])

        if current == three:
            score += inf
        elif current == two:
            score += 10
        elif current == one:
            score += 1
        elif current == three_opponent:
            score -= inf
        elif current == two_opponent:
            score -= 10
        elif current == one_opponent:
            score -= 1
    return score


def evaluate(state, last_move, player):
    # evaluate heuristic value of the entire game
    global box_won
    score = 0
    score += evaluate_big_box(box_won, player) * 100
    for b in range(9):
        idxs = indices_of_box(b)
        box_str = state[idxs[0]: idxs[-1] + 1]
        score += evaluate_small_box(box_str, player)
    return score


def minimax(state, last_move, player, depth, s_time):
    # minimax algorithm with alpha-beta pruning
    succ = successors(state, player, last_move)
    best_move = (-inf, None)
    for s in succ:
        val = min_turn(s[0], s[1], opponent(player), depth - 1, s_time,
                       -inf, inf)
        if val >= best_move[0]:
            best_move = (val, s)
    #        print("val = ", val)
    #        print_board(s[0])
    return best_move[1]


def min_turn(state, last_move, player, depth, s_time, alpha, beta):
    # represents the minimizing player who tries to reduce the maximum score the opponent can achieve
    global box_won
    if depth <= 0 or check_small_box(
            box_won) != "0":  # or time() - s_time >= 10: because they did not specified the time to play
        return evaluate(state, last_move, opponent(player))
    succ = successors(state, player, last_move)
    for s in succ:
        val = max_turn(s[0], s[1], opponent(player), depth - 1, s_time,
                       alpha, beta)
        if val < beta:
            beta = val
        if alpha >= beta:
            break
    return beta


def max_turn(state, last_move, player, depth, s_time, alpha, beta):
    # represents the maximizzing player who tries to increase their maximum score
    global box_won
    if depth <= 0 or check_small_box(
            box_won) != "0":  # or time() - s_time >= 20: because they did not specified the time to play
        return evaluate(state, last_move, player)
    succ = successors(state, player, last_move)
    for s in succ:
        val = min_turn(s[0], s[1], opponent(player), depth - 1, s_time,
                       alpha, beta)
        if alpha < val:
            alpha = val
        if alpha >= beta:
            break
    return alpha


#def valid_input(state, move):
#    # check if the move played is valid
#    global box_won
#    if not (0 < move[0] < 10 and 0 < move[1] < 10):
#        return False
#    if box_won[box(move[0], move[1])] != "0":
#        return False
#    if state[index(move[0], move[1])] != "0":
#        return False
#    return True


def who_is_player(redPlaying):
    if redPlaying:
        indice_player = '1'
        indice_bot = '2'
    else:
        indice_bot = '1'
        indice_player = '2'
    return (indice_player, indice_bot)


def bot(user_state, user_move, indice_bot, depth):
    global box_won, possible_goals
    if user_state == "0" * 81:
        return ("0" * 40 + indice_bot + "0" * 40, 40)
    s_time = time()
    bot_state, bot_move = minimax(user_state, user_move, indice_bot, depth, s_time)
    box_won = update_box_won(bot_state)

    return (bot_state, bot_move)


def joueur(bot_state, bot_move, last_move, indice_player):
    global box_won, possible_goals
    xcord, ycord = last_move
    user_move = ycord + 1, xcord + 1
    user_state = add_piece(bot_state, user_move, indice_player)
    box_won = update_box_won(user_state)

    return (user_state, user_move)



