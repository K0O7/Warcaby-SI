class Piece:
    # lista ruchów pionka białego
    white_moves = [(-1, -1), (-1, 1)]
    # lista ruchów pionka czarnego
    black_moves = [(1, -1), (1, 1)]
    # lista bić pionka
    hits = [(2, 2), (2, -2), (-2, -2), (-2, 2)]
    # lista ruchów królówki
    queen_moves = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                   (2, 2), (2, -2), (-2, 2), (-2, -2),
                   (3, 3), (3, -3), (-3, 3), (-3, -3),
                   (4, 4), (4, -4), (-4, 4), (-4, -4),
                   (5, 5), (5, -5), (-5, 5), (-5, -5),
                   (6, 6), (6, -6), (-6, 6), (-6, -6),
                   (7, 7), (7, -7), (-7, 7), (-7, -7)]
    queen_hits = [(2, 2), (2, -2), (-2, 2), (-2, -2),
                   (3, 3), (3, -3), (-3, 3), (-3, -3),
                   (4, 4), (4, -4), (-4, 4), (-4, -4),
                   (5, 5), (5, -5), (-5, 5), (-5, -5),
                   (6, 6), (6, -6), (-6, 6), (-6, -6),
                   (7, 7), (7, -7), (-7, 7), (-7, -7)]

    def __init__(self, is_white, is_queen):
        # flaga czy pinek jest czarny czy biały
        self.is_white = is_white
        # flaga czy jest królówką czy nie
        self.is_queen = is_queen

    def is_valid_move(self, start_position,
                      end_position):  # metoda przyjmójąca ruch i sprawdzająca czy teoretycznie możliwy
        if self.is_queen:
            for move in self.queen_moves:
                if start_position[0] + move[0] == end_position[0] and start_position[1] + move[1] == end_position[1]:
                    return 0
        else:
            if self.is_white:
                for move in self.white_moves:
                    if start_position[0] + move[0] == end_position[0] \
                            and start_position[1] + move[1] == end_position[1]:
                        return 0
            else:
                for move in self.black_moves:
                    if start_position[0] + move[0] == end_position[0] \
                            and start_position[1] + move[1] == end_position[1]:
                        return 0

        for move in self.hits:
            if start_position[0] + move[0] == end_position[0] and start_position[1] + move[1] == end_position[1]:
                return 1

        return -1

    def __repr__(self):
        return str(self)

    def __str__(self):
        string = " "

        if self.is_white:
            string += "W "
        else:
            string += "B "
        if self.is_queen:
            l = list(string)
            l[2] = "Q"
            string = "".join(l)

        return string
