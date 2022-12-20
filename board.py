import math
import random
import time
from copy import deepcopy, copy

from piece import Piece
from si_logic import min_max, alfa_beta


class Board:
    def __init__(self, x, y, is_player, is_player_white=True, heuristic_num_white=0 , heuristic_num_black=0, is_min_max_white = True, is_min_max_black = True, is_first_move_random = True, search_depth_white = 5, search_depth_black = 5, is_first_move_set = False, chosen_first_move = 0):
        # lista list zawierające pionki (obiekty piece)
        self.board = []
        # color = 0
        color = -1
        for i in range(x):
            if i == 0 or i == 1:
                color = 0

            if i == (x - 2) or i == (x - 1):
                color = 1

            if 1 < i < x - 2:
                color = -1

            temp_line = []
            for j in range(y):
                if color == -1:
                    temp_line.append('-')
                else:
                    is_white = False
                    if color == 1:
                        is_white = True

                    if i % 2 == 0:
                        if j % 2 == 0:
                            temp_line.append('-')
                        else:
                            temp_line.append(Piece(is_white, False))
                    else:
                        if j % 2 == 0:
                            temp_line.append(Piece(is_white, False))
                        else:
                            temp_line.append('-')
            self.board.append(temp_line)

        # self.board[7][6] = Piece(True, True)
        # self.board[6][5] = Piece(False, False)
        # self.board[1][3] = Piece(False,False)
        # self.board[2][5] = Piece(False, False)
        # self.board[2][3] = Piece(False,False)
        # self.board[1][1] = Piece(False, False)
        # self.board[4][3] = Piece(True, False)
        # self.board[4][5] = Piece(True, False)
        # self.board[4][1] = Piece(True, False)
        # self.board[5][2] = Piece(False, False)
        # self.board[3][4] = Piece(False, False)
        # self.board[5][4] = Piece(False, False)
        # self.board[6][5] = 0
        # self.board[3][6] = Piece(False, False)

        # flaga bool oznaczająca czyja jest tura
        self.is_white_turn = True

        # lista stanów plansz (historia rozgrywki)
        self.game_history = []
        self.game_history.append(self.board)

        # licznik ruchów do remisu
        self.moves_to_drow = 15
        self.drow = 15

        # flaga czy rozgrywka SI vs gracz czy SI vs SI
        self.is_SIvsPC = is_player

        # flaga czy gracz jest biały czy czarny
        self.player_as_white = is_player_white

        # znacznik jakiej heurystyki oceny używam
        self.using_heur_num_white = heuristic_num_white
        self.using_heur_num_black = heuristic_num_black

        # czy jest już damka na planszy
        self.is_queen = False

        self.is_min_max_white = is_min_max_white
        self.is_min_max_black = is_min_max_black

        self.depth_white = search_depth_white
        self.depth_black = search_depth_black

        if is_first_move_random:
            print(self)
            self.first_move_random()
            print(self)
        else:
            if is_first_move_set:
                print(self)
                self.first_move_set(chosen_first_move)
                print(self)

    def start_game(self):
        game_in_progress = True
        number_of_white_moves = 0
        number_of_black_moves = 0
        start_time = time.time()
        while game_in_progress:
            if self.is_SIvsPC:
                if self.player_as_white:
                    self.player_move()
                else:
                    self.SI_move()
            else:
                self.SI_move()

            number_of_white_moves += 1
            print(self)
            game_in_progress, res = self.check_winner()
            if game_in_progress:
                if res == "remis":
                    print(res)
                else:
                    print(res)
                return res, number_of_white_moves, time.time() - start_time

            # input("nacisnij enter aby kontynuowac")

            if self.is_SIvsPC:
                if self.player_as_white:
                    self.SI_move()
                else:
                    self.player_move()
            else:
                self.SI_move()

            number_of_black_moves += 1
            print(self)
            game_in_progress, res = self.check_winner()
            if game_in_progress:
                if res == "remis":
                    print(res)
                else:
                    print(res)
                return res, number_of_black_moves, time.time() - start_time
            game_in_progress = True
            # input("nacisnij enter aby kontynuowac")

    def check_winner(self):  # metoda sprawdzająca czy dla obecnego stanu planszy jest zwycięsca
        board_size = len(self.board)
        is_there_my_piece = False

        for i in range(board_size):  # brak pionków
            for j in range(board_size):
                if self.is_my_piece(i, j):
                    is_there_my_piece = True
        if not is_there_my_piece:
            if self.is_white_turn:
                return True, "wygrywa czarny"
            else:
                return True, "wygrywa bialy"

        if len(self.all_possible_moves()[0]) == 0:  # brak możliwych ruchów (sprawdzane za pomocą all_posible_moves)
            if self.is_white_turn:
                return True, "wygrywa czarny"
            else:
                return True, "wygrywa bialy"

        if self.moves_to_drow == 0:
            return True, "remis"

        return False, ""

    def player_move(self):  # metoda przyjmująca i wykonująca ruch gracza
        print("player moves")
        is_move_incorrect = True
        hit_chains = self.find_longest_hit_chain
        moved_queen = False
        while is_move_incorrect:
            try:
                move = input("wybierz ruch (pozycja startowa - pozycja końcowa np 2a-3b)")
                sp_ep = move.split('-')
                start_point = (int(sp_ep[0][0]) - 1, (ord(sp_ep[0][1]) - 97))
                end_point = (int(sp_ep[1][0]) - 1, (ord(sp_ep[1][1]) - 97))
                if self.board[start_point[0]][start_point[1]].is_queen:
                    moved_queen = True
                if self.is_my_piece(start_point[0], start_point[1]) and self.is_empty(end_point[0], end_point[1]):
                    move_type = self.board[start_point[0]][start_point[1]].is_valid_move(start_point, end_point)
                    if move_type == 0 and len(hit_chains) == 0:
                        # przesun pionek

                        if len(hit_chains) == 0:
                            self.move_piece(start_point, end_point, False)
                        else:
                            raise Exception

                        is_move_incorrect = False

                    if move_type == 1 or len(hit_chains) != 0:
                        is_in_chain = False
                        new_hit_chains = []
                        for hit in hit_chains:
                            if start_point in hit and end_point in hit:
                                is_in_chain = True
                                hit.pop(0)
                                new_hit_chains.append(hit)
                        hit_chains = new_hit_chains
                        _, between = self.chceck_in_beetween(start_point, end_point)
                        if is_in_chain:
                            self.move_piece(start_point, end_point, True, between)

                        else:
                            raise Exception

                        longest_list = max(len(elem) for elem in hit_chains)
                        if 1 == longest_list:
                            is_move_incorrect = False
                        else:
                            print(self)
                        # porównaj czy nalerzy do najdluzszego hit chaina
                        # jezeli tak to przesuń
                        # jeżeli hit chain się nie skończył topoinformuj gracza o tym ze dalej może bic
                        # rób to w pentli dopuki nie skończy się możliwość bicia

                    if move_type == -1:
                        raise Exception
            except:
                print("invalid move")
                is_move_incorrect = True
        if moved_queen:
            self.moves_to_drow -= 1
        else:
            self.moves_to_drow = self.drow

        self.is_white_turn = not self.is_white_turn
        self.update_queens()

    def SI_move(self):  # metoda wykonująca ruch SI
        print("si moves")
        if self.is_white_turn:
            if self.is_min_max_white:
                score, solution = min_max(self, self.is_white_turn, self.depth_white)
            else:
                score, solution = alfa_beta(self, self.is_white_turn, self.depth_white, -math.inf, math.inf)
        else:
            if self.is_min_max_black:
                score, solution = min_max(self, self.is_white_turn, self.depth_black)
            else:
                score, solution = alfa_beta(self, self.is_white_turn, self.depth_black, -math.inf, math.inf)

        moves, type_move = self.all_possible_moves()
        move = moves[solution]

        moved_queen = False
        if self.board[move[0][0]][move[0][1]].is_queen:
            moved_queen = True

        if type_move == 0:
            self.move_piece(move[0], move[1], False)
        else:
            for i in range((len(move) - 1)):
                _, between = self.chceck_in_beetween(move[i], move[i + 1])
                self.move_piece(move[i], move[i + 1], True, between)

        if moved_queen:
            self.moves_to_drow -= 1
        else:
            self.moves_to_drow = self.drow

        self.is_white_turn = not self.is_white_turn
        self.update_queens()

    def all_possible_moves(self):  # metoda zwracająca liste wszystkich możliwych ruchów gracza
        board_size = len(self.board)
        all_possible_moves = self.find_longest_hit_chain
        if len(all_possible_moves) > 0:
            return all_possible_moves, 1
        else:
            all_possible_moves = []

        for i in range(board_size):
            for j in range(board_size):
                if self.is_my_piece(i, j):
                    if self.board[i][j].is_queen:
                        all_moves = self.board[i][j].queen_moves
                    else:
                        if self.is_white_turn:
                            all_moves = self.board[i][j].white_moves
                        else:
                            all_moves = self.board[i][j].black_moves

                    for move in all_moves:
                        coordinates = ((move[0] + i), (move[1] + j))
                        if 0 <= coordinates[0] < board_size and 0 <= coordinates[1] < board_size:
                            if self.is_empty(coordinates[0], coordinates[1]) and not self.chceck_in_beetween((i, j), (coordinates[0], coordinates[1]))[0]:
                                temp_list = [(i, j), coordinates]
                                all_possible_moves.append(temp_list)

        return all_possible_moves, 0

    @property
    def find_longest_hit_chain(self):  # zwraca liste ruchów najdłuższego bicia, w przypadku remisu, wszystkie możliwe.
        hit_chains = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.is_my_piece(i, j):
                    # temp_board = deepcopy(self.board)
                    if self.board[i][j].is_queen:
                        temp_chain = self.is_there_hit(i, j, self.board[i][j].queen_hits, [], [], [], 0)
                    else:
                        temp_chain = self.is_there_hit(i, j, self.board[i][j].hits, [], [], [], 0)

                    # self.board = temp_board
                    if not len(temp_chain[0]) == 1:
                        if not hit_chains:
                            hit_chains = temp_chain
                        else:
                            for hit in temp_chain:
                                hit_chains.append(hit)

        new_hit_chains = []
        if hit_chains:
            longest_list = max(len(elem) for elem in hit_chains)
            for hit in hit_chains:
                if len(hit) == longest_list:
                    new_hit_chains.append(hit)
            hit_chains = new_hit_chains
        return hit_chains

    def is_there_hit(self, i, j, hits, prev_hited, temp_chain, temp_chains, chain_num):
        my_temp_chain = copy(temp_chain)
        my_temp_chain.append((i, j))

        next_possible_moves = []
        enemys_between = []
        for move in hits:
            temp_x_y = (i + move[0], j + move[1])
            if 0 <= temp_x_y[0] < 8 and 0 <= temp_x_y[1] < 8:
                is_there_enemy, beetwen_x_y = self.chceck_in_beetween((i, j), temp_x_y)
                if is_there_enemy and self.is_empty(temp_x_y[0], temp_x_y[1]):
                    if beetwen_x_y not in prev_hited:
                        next_possible_moves.append(temp_x_y)
                        enemys_between.append(beetwen_x_y)

        crossroad = 0
        temp_board = copy(self.board)
        new_prev_hited = copy(prev_hited)
        for move in next_possible_moves:
            new_prev_hited.append(enemys_between[crossroad])
            self.is_there_hit(move[0], move[1], hits, new_prev_hited, my_temp_chain, temp_chains, chain_num + crossroad)
            crossroad += 1
            self.board = temp_board

        if len(next_possible_moves) == 0:
            temp_chains.append(my_temp_chain)

        return temp_chains

    def chceck_in_beetween(self, start, dest):
        x_sign = 1
        y_sign = 1
        temp = ((dest[0] - start[0]), (dest[1] - start[1]) )
        start_copy = copy(start)
        if temp[0] < 0:
            x_sign *= -1
        if temp[1] < 0:
            y_sign *= -1

        pos_of_enem = []
        while start_copy != dest:
            start_copy = (start_copy[0] + x_sign), (start_copy[1] + y_sign)
            if self.is_enemy(start_copy[0], start_copy[1]):
                pos_of_enem.append(copy(start_copy))

        if len(pos_of_enem) == 1:
            return True, pos_of_enem[0]
        else:
            return False, (-1, -1)

    def judge_board_one(self):  # heurystyka nr. 1
        field_one = [0, 7, 0, 7]  # pierwszy obszar punktowany
        field_two = [1, 6, 1, 6]  # drugi obszar punktowany
        field_three = [2, 5, 2, 5]  # trzeci obszar punktowany
        score = 0
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                in_field_three = False
                in_field_two = False
                in_field_one = False
                if not self.is_empty(i, j):
                    if field_three[0] <= i <= field_three[1] and field_three[2] <= j <= field_three[3]:
                        in_field_three = True
                    if field_two[0] <= i <= field_two[1] and field_two[2] <= j <= field_two[3] and not in_field_three:
                        in_field_two = True
                    if field_one[0] <= i <= field_one[1] and field_one[2] <= j <= field_one[3] and not in_field_two:
                        in_field_one = True

                    multiplayer = 1

                    if self.is_enemy(i, j):
                        multiplayer *= -1

                    if self.board[i][j].is_queen:
                        multiplayer *= 8

                    if in_field_three:
                        score += 1 * multiplayer
                    if in_field_one:
                        score += 4 * multiplayer
                    if in_field_two:
                        score += 2 * multiplayer
        return score

    def judge_board_two(self):  # heurystyka nr. 1
        score = 0
        queen_weight = 5
        my_moves, my_type = self.all_possible_moves()
        self.is_white_turn = not self.is_white_turn
        enemy_moves, enemy_type = self.all_possible_moves()
        self.is_white_turn = not self.is_white_turn

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.is_my_piece(i, j):
                    if self.board[i][j].is_queen:
                        score += 1 * queen_weight
                    else:
                        score += 2
                else:
                    if self.is_enemy(i, j):
                        if self.board[i][j].is_queen:
                            score -= 1 * queen_weight
                        else:
                            score -= 2

        if my_type == 0:
            score += len(my_moves)
        else:
            score += len(my_moves)*len(my_moves[0])

        if enemy_type == 0:
            score -= len(enemy_moves)
        else:
            score -= len(enemy_moves) * len(enemy_moves[0])

        return score

    def is_empty(self, x, y):
        x = int(x)
        y = int(y)
        return self.board[x][y] == '-'

    def is_enemy(self, x, y):
        x = int(x)
        y = int(y)
        if type(self.board[x][y]) is Piece:
            return self.board[x][y].is_white == (not self.is_white_turn)
        else:
            return False

    def is_my_piece(self, x, y):
        x = int(x)
        y = int(y)
        if type(self.board[x][y]) is Piece:
            return self.board[x][y].is_white == self.is_white_turn
        else:
            return False

    def update_queens(self):
        for i in range(len(self.board)):
            if not self.is_empty(0, i):
                if self.board[0][i].is_white:
                    self.board[0][i].is_queen = True
                    self.is_queen = True
            if not self.is_empty(len(self.board) - 1, i):
                if not self.board[len(self.board) - 1][i].is_white:
                    self.board[len(self.board) - 1][i].is_queen = True
                    self.is_queen = True

    def move_piece(self, start_point, end_point, is_hit, beetwen_x_y=(-1, -1)):
        if is_hit:
            self.board[end_point[0]][end_point[1]] = self.board[start_point[0]][start_point[1]]
            self.board[start_point[0]][start_point[1]] = '-'
            # beetwen_x_y = (
            #     (-start_point[0] + end_point[0]) / 2, (-start_point[1] + end_point[1]) / 2)
            # self.board[int(start_point[0] + beetwen_x_y[0])][
            #     int(start_point[1] + beetwen_x_y[1])] = '-'
            self.board[beetwen_x_y[0]][beetwen_x_y[1]] = '-'
        else:
            self.board[end_point[0]][end_point[1]] = self.board[start_point[0]][start_point[1]]
            self.board[start_point[0]][start_point[1]] = '-'
        # self.game_history.append(deepcopy(self.board))

    def chosen_heur(self):
        if self.is_white_turn:
            if self.using_heur_num_white == 0:
                return self.judge_board_one()
            if self.using_heur_num_white == 1:
                return self.judge_board_two()
        else:
            if self.using_heur_num_black == 0:
                return self.judge_board_one()
            if self.using_heur_num_black == 1:
                return self.judge_board_two()

    def first_move_random(self):
        print("random move")
        moves, _ = self.all_possible_moves()
        size = len(moves)
        index = random.randrange(0, size)
        self.move_piece(moves[index][0], moves[index][1], False)
        self.is_white_turn = not self.is_white_turn

    def first_move_set(self, index):
        print("random move")
        moves, _ = self.all_possible_moves()
        self.move_piece(moves[index][0], moves[index][1], False)
        self.is_white_turn = not self.is_white_turn

    def __repr__(self):
        return str(self)

    def __str__(self):
        string = "    a    b    c    d    e    f    g    h\n"
        for i in range(len(self.board)):
            string += str((i + 1)) + " " + str(self.board[i]) + "\n"
        return string
