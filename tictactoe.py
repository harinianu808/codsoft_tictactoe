import math
import os

EMPTY = " "
AI_PLAYER = "O"
HUMAN_PLAYER = "X"


def print_board(board):
    """Renders the current board state to the console."""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def is_winner(board, player):
    """Checks if the given player has won the game."""
    win_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],  # Rows
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],  # Columns
        [0, 4, 8],
        [2, 4, 6],  # Diagonals
    ]
    return any(all(board[cell] == player for cell in combo) for combo in win_conditions)


def is_board_full(board):
    """Returns True if there are no empty spaces left."""
    return EMPTY not in board


def get_empty_cells(board):
    """Returns a list of indices that are empty."""
    return [i for i, cell in enumerate(board) if cell == EMPTY]


def minimax(board, depth, is_maximizing):
    """The core Minimax algorithm."""
    # Base cases: Terminal states (Win, Loss, Draw)
    if is_winner(board, AI_PLAYER):
        return 10 - depth  # Subtract depth to favor faster wins
    if is_winner(board, HUMAN_PLAYER):
        return depth - 10  # Add depth to favor longer survival
    if is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for cell in get_empty_cells(board):
            board[cell] = AI_PLAYER
            score = minimax(board, depth + 1, False)
            board[cell] = EMPTY  # Undo move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for cell in get_empty_cells(board):
            board[cell] = HUMAN_PLAYER
            score = minimax(board, depth + 1, True)
            board[cell] = EMPTY  # Undo move
            best_score = min(score, best_score)
        return best_score


def find_best_move(board):
    """Evaluates all available moves and returns the best one for the AI."""
    best_score = -math.inf
    best_move = None

    for cell in get_empty_cells(board):
        board[cell] = AI_PLAYER
        move_score = minimax(board, 0, False)
        board[cell] = EMPTY  # Undo move

        if move_score > best_score:
            best_score = move_score
            best_move = cell

    return best_move


def play_game():
    """Main game loop."""
    board = [EMPTY] * 9
    print("Welcome to Unbeatable Tic-Tac-Toe!")
    print("Positions are numbered 1-9 from top-left to bottom-right.")

    # Human plays X (goes first), AI plays O
    while True:
        print_board(board)

        # --- Human Turn ---
        while True:
            try:
                move = (
                    int(input("Enter your move (1-9) or 0 to exit: ")) - 1
                )
                if move == -1:
                    print("Game exited.")
                    return
                if move in range(9) and board[move] == EMPTY:
                    board[move] = HUMAN_PLAYER
                    break
                else:
                    print("Invalid move. The cell is either taken or out of bounds.")
            except ValueError:
                print("Please enter a valid number between 1 and 9.")

        # Check if Human won or drew
        if is_winner(board, HUMAN_PLAYER):
            print_board(board)
            print("Wait... you won? That shouldn't happen. Logic error!")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw! (The best possible outcome against this AI)")
            break

        # --- AI Turn ---
        ai_move = find_best_move(board)
        if ai_move is not None:
            board[ai_move] = AI_PLAYER

        # Check if AI won or drew
        if is_winner(board, AI_PLAYER):
            print_board(board)
            print("AI wins! Better luck next time.")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break


if __name__ == "__main__":
    play_game()