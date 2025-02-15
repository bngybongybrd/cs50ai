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
    count_x = 0
    count_o = 0

    # counts number of X and O on board
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1
    
    # board full
    if count_x + count_o == 9:
        return -1

    # empty board
    if count_x == count_o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    free = set()

    count_x = 0
    count_o = 0

    # counts number of X and O on board
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_x += 1
            elif board[i][j] == O:
                count_o += 1
            elif board[i][j] == EMPTY: # EMPTY
                free.add((i, j))

    # board full
    if count_x + count_o == 9:
        return -1
    
    return free


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempboard = copy.deepcopy(board)

    if tempboard[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action")
    else:
        # finds which player's turn
        turn = player(board)
        if turn != -1:
            tempboard[action[0]][action[1]] = turn

    return tempboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        # check horizonal
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # check vertical
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
        
    # check diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2] and board[2][0] != EMPTY:
        return board[2][0]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # Board full or found winner
    if player(board) == -1 or winner(board) != None:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if player(board) == -1:
        return 0
    elif winner(board) == X:
        return 1
    else: # winner is O
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if board is terminal board
    if terminal(board):
        return None
    
    def maxval(board):
        if terminal(board):
            return [utility(board), None]
        v = -99999
        optimal = None
        for action in actions(board):
            value = minval(result(board, action))[0]
            if value > v:
                v = value
                optimal = action
        return [v, optimal]
    
    def minval(board):
        if terminal(board):
            return [utility(board), None]
        v = 99999
        optimal = None
        for action in actions(board):
            value = maxval(result(board, action))[0]
            if value < v:
                v = value
                optimal = action
        return [v, optimal]
    
    if player(board) == X:
        return maxval(board)[1]
    elif player(board) == O:
        return minval(board)[1]
