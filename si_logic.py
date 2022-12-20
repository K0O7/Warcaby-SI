import math
from copy import deepcopy


def min_max(board, original_player, depth):  # metoda zwracająca najlepszy możliwy do wykonania ruch wg algorytmu minimax
    is_winner, type = board.check_winner()
    if is_winner:  # rozdzielić i zrobić aby wygrana inf razy lepsza niż osiągniecie głębokości a przegrana inf razy gorsza

        if original_player == board.is_white_turn:
            if type != "remis":
                return math.inf, 0
            else:
                return -math.inf, 0
        else:
            return -math.inf, 0

    if depth == 0:
        return board.chosen_heur(), 0

    moves, type = board.all_possible_moves()
    scores = []
    if type == 0:
        for move in moves:
            new_board = deepcopy(board)
            new_board.move_piece(move[0], move[1], False)
            new_board.is_white_turn = (not new_board.is_white_turn)
            new_board.update_queens()
            scores.append(min_max(new_board, original_player, depth-1)[0])
    else:
        for move in moves:
            new_board = deepcopy(board)
            for i in range((len(move) - 1)):
                new_board.move_piece(move[i], move[i + 1], True)
            new_board.is_white_turn = (not new_board.is_white_turn)
            new_board.update_queens()
            scores.append(min_max(new_board, original_player, depth-1)[0])

    if original_player == board.is_white_turn:
        return max(scores), scores.index(max(scores))
    else:
        return min(scores), scores.index(min(scores))

def alfa_beta(board, original_player, depth, alfa, beta):  # metoda zwracająca najlepszy możliwy do wykonania ruch wg algorytmu minimax
    is_winner, type = board.check_winner()
    if is_winner:  # rozdzielić i zrobić aby wygrana inf razy lepsza niż osiągniecie głębokości a przegrana inf razy gorsza

        if original_player == board.is_white_turn:
            if type != "remis":
                return math.inf, 0
            else:
                return -math.inf, 0
        else:
            return -math.inf, 0

    if depth == 0:
        return board.chosen_heur(), 0

    moves, type = board.all_possible_moves()
    index = 0
    scores = []
    if original_player == board.is_white_turn:
        value = -math.inf
        if type == 0:
            for move in moves:
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1], False)
                new_board.is_white_turn = (not new_board.is_white_turn)
                new_board.update_queens()
                value = max(value, alfa_beta(new_board, original_player, depth - 1, alfa, beta)[0])
                scores.append(value)
                if value >= beta:
                    break
                alfa = max(alfa, value)
        else:
            for move in moves:
                new_board = deepcopy(board)
                for i in range((len(move) - 1)):
                    new_board.move_piece(move[i], move[i + 1], True)
                new_board.is_white_turn = (not new_board.is_white_turn)
                new_board.update_queens()
                value = max(value, alfa_beta(new_board, original_player, depth - 1, alfa, beta)[0])
                scores.append(value)
                if value >= beta:
                    break
                alfa = max(alfa, value)
        return max(scores), scores.index(max(scores))
    else:
        value = math.inf
        if type == 0:
            for move in moves:
                new_board = deepcopy(board)
                new_board.move_piece(move[0], move[1], False)
                new_board.is_white_turn = (not new_board.is_white_turn)
                new_board.update_queens()
                value = min(value, alfa_beta(new_board, original_player, depth - 1, alfa, beta)[0])
                scores.append(value)
                if value <= alfa:
                    break
                beta = min(beta, value)
        else:
            for move in moves:
                new_board = deepcopy(board)
                for i in range((len(move) - 1)):
                    new_board.move_piece(move[i], move[i + 1], True)
                new_board.is_white_turn = (not new_board.is_white_turn)
                new_board.update_queens()
                value = min(value, alfa_beta(new_board, original_player, depth - 1, alfa, beta)[0])
                scores.append(value)
                if value <= alfa:
                    break
                beta = min(beta, value)
        return min(scores), scores.index(min(scores))
