import random
import copy


class TETROMINO:
    def __init__(self, name, center, color_ind):
        self.name = name
        self.initial_rot = 0
        self.center = center
        self.color_ind = color_ind
        self.x = 45 + center[0]
        self.y = 14 + center[1]

    def rotate_left(self):
        self.initial_rot -= 1
        self.initial_rot = self.initial_rot % 4
        self.name = self.name[:-1] + str(self.initial_rot)

    def rotate_right(self):
        self.initial_rot += 1
        self.initial_rot = self.initial_rot % 4
        self.name = self.name[:-1] + str(self.initial_rot)


TETRIS_I = TETROMINO("tetris_i_0", center=(2, 0), color_ind="1")
TETRIS_J = TETROMINO("tetris_j_0", center=(0, 0), color_ind="2")
TETRIS_L = TETROMINO("tetris_l_0", center=(0, 0), color_ind="3")
TETRIS_O = TETROMINO("tetris_o_0", center=(0, 0), color_ind="4")
TETRIS_S = TETROMINO("tetris_s_0", center=(0, 0), color_ind="5")
TETRIS_T = TETROMINO("tetris_t_0", center=(0, 0), color_ind="6")
TETRIS_Z = TETROMINO("tetris_z_0", center=(0, 0), color_ind="7")

TETROMINOS = [
    TETRIS_I,
    TETRIS_J,
    TETRIS_L,
    TETRIS_O,
    TETRIS_S,
    TETRIS_T,
    TETRIS_Z,
]


class Tetris:
    def __init__(self, os):
        self.os = os
        self.current_bag = []
        self.refill_bag()
        self.current_piece = self.get_tetris_piece()
        self.next_piece = self.get_tetris_piece()
        self.board = [["0"] * 10] * 20
        self.i = 0

    def step(self, keypressed):
        """
        Game event loop
        """
        if self.i == 0:
            self.i = 0
            # print(self.board)
            score = self.os.get_score("tetris")
            self.os.blit("tetris_board", 0, 0)

            if keypressed[0]:  # hard drop
                pass
            elif keypressed[1]:  # left arrow key
                print("Moving left")
                self.current_piece.x = self.current_piece.x - 3

            elif keypressed[3]:  # right arrow key
                print("Moving right")
                self.current_piece.x = self.current_piece.x + 3

            if keypressed[4]:
                print("Rotate anticlockwise")
                self.current_piece.rotate_left()
            elif keypressed[5]:
                print("Rotate clockwise")
                self.current_piece.rotate_right()

            if keypressed[2]:  # down arrow key, soft drop # go fast logic here
                print("Going Fast!")
                self.current_piece.y = self.current_piece.y + 1
            else:
                self.current_piece.y = self.current_piece.y + 1

            if self.check_intersection(
                self.current_piece
            ):  # check intersection and if it intersects then add it to the board!
                self.add_tetromino_to_board(self.current_piece)
                self.current_piece = self.next_piece
                self.current_piece.x = 15
                # change the current piece to next one
                self.next_piece = self.get_tetris_piece()  # get the new next one
            else:
                self.os.blit(
                    self.current_piece.name, self.current_piece.x, self.current_piece.y
                )  # usual current piece blit

            self.os.blit(
                self.next_piece.name, self.next_piece.x, self.next_piece.y
            )  # blit the next piece in its place.

            self.os.display_num(score, 48, 39, align="right")  # display highscore
            # print(self.board)
            self.blit_board()
        else:
            self.i += 1

    def refill_bag(self):
        self.current_bag.extend(copy.deepcopy(TETROMINOS))
        random.shuffle(self.current_bag)

    def get_tetris_piece(self):
        if len(self.current_bag) == 0:
            self.refill_bag()
        return self.current_bag.pop(0)

    def clear_row(self, row_num):
        self.board[row_num] = ["0"] * 10
        # REMOVING A BLOCK ROW
        # TODO

    def get_pixel_loc_from_board_index(self, x, y):
        row = 1
        col = 1

        return row, col

    def check_intersection(self, tetromino):
        if tetromino.y == 65:
            return True
        return False

    def blit_board(self):
        for i in range(5, 33, 3):
            for j in range(10, 68, 3):
                col = (i - 5) // 3
                row = (j - 10) // 3
                if self.board[row][col] != "0":
                    self.os.blit("tetris_" + self.board[row][col], i, j)

    def add_tetromino_to_board(self, tetromino):
        # convert x and y to row and column of the board
        row = 4
        col = 7
        self.board[row][col] = tetromino.color_ind

    def die(self):
        pass
