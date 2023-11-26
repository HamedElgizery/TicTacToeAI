"""
Tic Tac Toe Player
"""

import math
from random import randint

X = "X"
O = "O"
EMPTY = None

class InvalidAction(Exception):
    pass


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
    count_X = 0
    count_O = 0
    for row in board:
        for cell in row:
            if cell == X:
                count_X += 1
            if cell == O:
                count_O += 1
    return X if count_X == count_O else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_available = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actions_available.add((i, j))
    return actions_available


def result(board, action):
    """
    returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] and action[0] < 3 and 0 <= action[1] and action[1] < 3) or board[action[0]][action[1]] is not None:
        raise InvalidAction(action)
    board[action[0]][action[1]] = player(board)
    return board


def undo_result(board, action):
    """
    returns the board after emptying the cell (i, j) on the board.
    """
    board[action[0]][action[1]] = EMPTY
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] != None and row[0] == row[1] and row[1] == row[2]:
            return row[0] 
    for i in range(3):
        if board[0][i] != None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i] 
    if board[0][0] != None and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0] 
    if board[2][0] != None and board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[2][0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    return 0


def maximize(board):
    if terminal(board):
        return utility(board), (-1, -1) 
    mx = -2
    opt_action = (-1, -1) 
    actions_available = actions(board)
    for i, action in enumerate(actions_available):
        mini_result = minimize(result(board, action))
        if mini_result[0] > mx or (mini_result == mx and randint(1, 3) == 2):
            opt_action = action 
            mx = mini_result[0]
        undo_result(board, action)
    return (mx, opt_action)


def minimize(board):
    if terminal(board):
        return utility(board), (-1, -1) 
    mn = 2
    opt_action = (0, 0)
    actions_available = actions(board)
    for i, action in enumerate(actions_available):
        maxi_result = maximize(result(board, action))
        if maxi_result[0] < mn or (maxi_result == mn and randint(1, 3) == 2):
            opt_action = action
            mn = maxi_result[0]
        undo_result(board, action)
    return (mn, opt_action)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    turn = player(board)
    if turn == X:
        return maximize(board)[1]
    else:
        return minimize(board)[1]
