import math

board_size = 3

# Function to print the Tic Tac Toe board
def print_board(board):
    print("-------------")
    for i in range(board_size):
        row = "| "
        for j in range(board_size):
            row += board[i * board_size + j] + " | "
        print(row)
        print("-------------")

# Function to check if the board is full
def is_board_full(board):
    return not ' ' in board

# Function to check for winner
def check_for_winner(board, marker):
    # Check rows
    for i in range(board_size):
        if all(board[i * board_size + j] == marker for j in range(board_size)):
            return True

    # Check columns
    for i in range(board_size):
        if all(board[i + j * board_size] == marker for j in range(board_size)):
            return True

    # Check diagonals
    if all(board[i * board_size + i] == marker for i in range(board_size)):
        return True

    if all(board[i * board_size + (board_size - 1 - i)] == marker for i in range(board_size)):
        return True

    return False

# Heuristic function to evaluate the score of the board
def evaluate_board(board):
    ai_score = 0
    player_score = 0

    # Evaluate rows
    for i in range(board_size):
        row = board[i * board_size:i * board_size + board_size]
        if row.count(ai_marker) == board_size:
            ai_score += 1
        elif row.count(player_marker) == board_size:
            player_score += 1

    # Evaluate columns
    for i in range(board_size):
        column = [board[j] for j in range(i, board_size ** 2, board_size)]
        if column.count(ai_marker) == board_size:
            ai_score += 1
        elif column.count(player_marker) == board_size:
            player_score += 1

    # Evaluate diagonals
    diagonal1 = [board[i] for i in range(0, board_size ** 2, board_size + 1)]
    diagonal2 = [board[i] for i in range(board_size - 1, board_size ** 2 - 1, board_size - 1)]
    if diagonal1.count(ai_marker) == board_size:
        ai_score += 1
    elif diagonal1.count(player_marker) == board_size:
        player_score += 1
    if diagonal2.count(ai_marker) == board_size:
        ai_score += 1
    elif diagonal2.count(player_marker) == board_size:
        player_score += 1

    return ai_score - player_score

# Heuristic search algorithm
def heuristic_search(board, depth, is_maximizing_player):
    if check_for_winner(board, ai_marker):
        return 10 - depth
    elif check_for_winner(board, player_marker):
        return depth - 10
    elif is_board_full(board):
        return 0

    if is_maximizing_player:
        best_score = -math.inf
        for i in range(board_size ** 2):
            if board[i] == ' ':
                board[i] = ai_marker
                score = heuristic_search(board, depth + 1, False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(board_size ** 2):
            if board[i] == ' ':
                board[i] = player_marker
                score = heuristic_search(board, depth + 1, True)
                board[i] = ' '
                best_score = min(best_score, score)
        return best_score

def play_game():
    global ai_marker, player_marker
    board = [' ' for _ in range(board_size ** 2)]
    # Set markers for AI and player
    ai_marker = input("Choose AI marker (X/O): ")
    player_marker = 'X' if ai_marker == 'O' else 'O'

    # Determine who goes first
    if ai_marker == 'X':
        current_player = "AI"
    else:
        current_player = "player"

    while True:
        if current_player == "AI":
            best_score = -math.inf
            best_move = None
            for i in range(board_size ** 2):
                if board[i] == ' ':
                    board[i] = ai_marker
                    score = heuristic_search(board, 0, False)
                    board[i] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = i
            board[best_move] = ai_marker
            current_player = "player"
        else:
            print_board(board)
            move = int(input("Choose a move (0-8): "))
            if board[move] != ' ':
                print("Invalid move")
                continue
            board[move] = player_marker
            current_player = "AI"

        if check_for_winner(board, ai_marker):
            print_board(board)
            print("AI wins!")
            break
        elif check_for_winner(board, player_marker):
            print_board(board)
            print("Player wins!")
            break
        elif is_board_full(board):
            print_board(board)
            print("It's a tie!")
            break

play_game()
