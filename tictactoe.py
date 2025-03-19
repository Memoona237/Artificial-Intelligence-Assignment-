import math

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
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid move!")
    
    new_board = [row[:] for row in board]  # Create a copy of the board
    new_board[i][j] = player(board)  # Make the move for the current player
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    
    return None  # No winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(board[i][j] is not EMPTY for i in range(3) for j in range(3))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None  # No move to make if the game is over

    current_player = player(board)
    
    if current_player == X:
        # Maximize X's score
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            value = minimax_value(new_board)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        # Minimize O's score
        best_value = math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            value = minimax_value(new_board)
            if value < best_value:
                best_value = value
                best_action = action
        return best_action


def minimax_value(board):
    """
    Helper function to return the minimax value for a given board.
    """
    if terminal(board):
        return utility(board)
    
    current_player = player(board)
    
    if current_player == X:
        # Maximize X's score
        best_value = -math.inf
        for action in actions(board):
            new_board = result(board, action)
            value = minimax_value(new_board)
            best_value = max(best_value, value)
        return best_value
    else:
        # Minimize O's score
        best_value = math.inf
        for action in actions(board):
            new_board = result(board, action)
            value = minimax_value(new_board)
            best_value = min(best_value, value)
        return best_value

