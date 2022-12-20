from board import Board
import sys

if __name__ == '__main__':
    sys.setrecursionlimit(5000)
    game = Board(x=8, y=8, is_player=False, heuristic_num_white=0, is_min_max_white=False, is_min_max_black=False, is_first_move_random=True, search_depth_white=5, search_depth_black=5)
