import random

#                       USAGE!
#             ( '>' sign means user input )
#   Input command: > start [mode] [mode]                // available modes:
#                            /|\    /|\                 // user - you play as
#                             |      |                  // easy - computer (difficulty easy)
#                        1st move  2nd move             // medium - computer (difficulty medium)
#                                                       // hard - computer (difficulty hard)

#               WHEN PLAYING AS USER!:
#   Enter the coordinates: > [x] [y]                    // don't forget about space!
#      O --->   x
#      |      1 2 3
#      v    ---------
#         3 | _ _ _ |
#     y   2 | _ _ _ |
#         1 | _ _ _ |
#           ---------


def display_board():
    print(9 * '-')
    for i in range(0, 9, 3):
        print('|', *board[i: i + 3], '|')
    print(9 * '-')


def move_user(symbol):
    while True:
        move = input('Enter the coordinates: ').split()
        x, y = move if len(move) == 2 else ('x', 'y')

        if not x.isnumeric() or not y.isnumeric():
            print('You should enter numbers!')
        elif x not in ('1', '2', '3') or y not in ('1', '2', '3'):
            print('Coordinates should be from 1 to 3!')
        elif board[(3 - int(y)) * 3 + (int(x) - 1)] != ' ':
            print('This cell is occupied! Choose another one!')
        else:
            board[(3 - int(y)) * 3 + (int(x) - 1)] = symbol
            break


def move_easy(symbol, signal=True):
    if signal:
        print('Making move level "easy"')

    while True:
        x, y = random.randint(1, 3), random.randint(1, 3)

        if board[(3 - y) * 3 + (x - 1)] == ' ':
            board[(3 - y) * 3 + (x - 1)] = symbol
            break


def medium_input(symbol):
    def check_for(num_s, num_z):
        for i in range(8):
            if winlane[i].count(s) == num_s and winlane[i].count(z) == num_z:
                for j in moves[i]:
                    if board[j] == ' ':
                        board[j] = s
                return True

    print('Making move level "medium"')

    s, z = ('X', 'O') if symbol == 'X' else ('O', 'X')
    winlane = [board[:3], board[3:6], board[6:], board[::3], board[1::3], board[2::3], board[::4], board[2:7:2]]
    moves = [range(3), range(3, 6), range(6, 9), range(0, 9, 3), range(1, 9, 3), range(2, 9, 3), range(0, 9, 4), range(2, 7, 2)]
    moves = [list(x) for x in moves]

    if check_for(2, 0):
        return None
    elif check_for(0, 2):
        return None
    else:
        move_easy(symbol, signal=False)


def hard_input(symbol):
    print('Making move level "hard"')
    global ai, hu
    ai = symbol
    hu = 'O' if symbol == 'X' else 'X'
    board[minimax(symbol)[1]] = symbol


def win(symbol):
    rules = [board[:3], board[3:6], board[6:], board[::3], board[1::3], board[2::3], board[::4], board[2:7:2]]

    if 3 * [symbol] in rules:
        return True
    return False


def minimax(player):
    global board

    if win(hu):
        return -10, None
    elif win(ai):
        return 10, None
    elif board.count(' ') == 0:
        return 0, None

    moves = []

    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            res = minimax(hu) if player == ai else minimax(ai)
            move = (res[0], i)
            board[i] = ' '

            moves.append(move)

    return min(moves) if player == hu else max(moves)


def make_move(symbol):
    players[symbol](symbol)


def check_state(symbol):
    rules = [board[:3], board[3:6], board[6:], board[::3], board[1::3], board[2::3], board[::4], board[2:7:2]]
    display_board()

    if 3 * [symbol] in rules:
        print(f'{symbol} wins')
    elif ' ' not in board:
        print('Draw')
    else:
        return True


def game():
    s, z = 'X', 'O'
    display_board()

    while True:
        make_move(s)
        if not check_state(s):
            break
        s, z = z, s


options = {'user': move_user, 'easy': move_easy, 'medium': medium_input, 'hard': hard_input}

while True:
    action = input('Input command: ').split()

    if action[0] == 'exit':
        break
    elif len(action) == 3 and action[0] == 'start' and action[1] in options and action[2] in options:
        board = [' '] * 9
        players = {'X': options[action[1]], 'O': options[action[2]]}
        game()
    else:
        print('Bad parameters!')
