"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if(board == initial_state()): # Game is in the initial state
        return X
    if(terminal(board)): # Game is over
        return None
    # Count the number of "X" and the number of "O": if count_X > count_O return "O" else return "X"
    count_X, count_O = 0, 0
    for row in board:
        for val in row:
            if(val == "X"):
                count_X += 1
            elif(val == "O"):
                count_O += 1
    if(count_X > count_O):
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if(terminal(board)): # Game is over
        return None
    # Find all coordinates on the board that are None, and return a set of those coordinates
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == None):
                actions.add((i,j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board) # Either "X" or "O"
    if(board[action[0]][action[1]] != None):
        raise Exception
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = p
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # 3 rows, 3 cols, 2 diagonals
    coord_matrix = [[(0,0), (0,1), (0,2)], # row0
                    [(1,0), (1,1), (1,2)], # row1
                    [(2,0), (2,1), (2,2)], # row2
                    [(0,0), (1,0), (2,0)], # col0
                    [(0,1), (1,1), (2,1)], # col1
                    [(0,2), (1,2), (2,2)], # col2
                    [(0,0), (1,1), (2,2)], # diag0
                    [(0,2), (1,1), (2,0)]] # diag1
    for coord0, coord1, coord2 in coord_matrix:
        if(board[coord0[0]][coord0[1]] == board[coord1[0]][coord1[1]] == board[coord2[0]][coord2[1]] and board[coord0[0]][coord0[1]] != None):
            return board[coord0[0]][coord0[1]]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    flag_None = 0
    for row in board:
        for val in row:
            if(val == None):
                flag_None = 1 # If flag = 1 -> result is pending, not draw
    w = winner(board)
    if(w != None or (w == None and flag_None == 0)): # someone already won or it is a Draw (no more moves to make)
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if(w == X):
        return 1
    elif(w == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)): # Game is over
        return None
    p = player(board) # X is max player, O is min player
    action_to_return = None
    if (p == X):
        value = -math.inf
        for action in actions(board):
            val = min_value(result(board, action))
            if(val > value):
                value = val
                action_to_return = action
    else:
        value = math.inf
        for action in actions(board):
            val = max_value(result(board, action))
            if(val < value):
                value = val
                action_to_return = action
    return action_to_return


def min(x, y):
    '''
    Returns the minimum value.
    '''
    return x if x < y else y


def max(x, y):
    '''
    Returns the maximum value.
    '''
    return x if x > y else y


def max_value(board):
    '''
    Helper Function for minimax().
    '''
    if(terminal(board)):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    '''
    Helper Function for minimax().
    '''
    if(terminal(board)):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value