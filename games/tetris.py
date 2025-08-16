import random
import copy


class TETROMINO:
    def __init__(self, name, center, color_ind, geometry):
        self.name = name
        self.initial_rot = 0
        self.center = center
        self.color_ind = color_ind
        self.x = 45 + center[0]
        self.y = 14 + center[1]
        self.geometry = geometry  # based on (row,col)

    def rotate_left(self):
        self.initial_rot -= 1
        self.initial_rot = self.initial_rot % 4
        self.name = self.name[:-1] + str(self.initial_rot)

    def rotate_right(self):
        self.initial_rot += 1
        self.initial_rot = self.initial_rot % 4
        self.name = self.name[:-1] + str(self.initial_rot)


TETRIS_I = TETROMINO(
    "tetris_i_0",
    center=(0, 0),
    color_ind="1",
    geometry=[(0, 0), (1, 0), (2, 0), (3, 0)],
)
TETRIS_J = TETROMINO(
    "tetris_j_0",
    center=(0, 0),
    color_ind="2",
    geometry=[(0, 1), (1, 1), (2, 1), (2, 0)],
)
TETRIS_L = TETROMINO(
    "tetris_l_0",
    center=(0, 0),
    color_ind="3",
    geometry=[(0, 0), (1, 0), (2, 0), (2, 1)],
)
TETRIS_O = TETROMINO(
    "tetris_o_0",
    center=(0, 0),
    color_ind="4",
    geometry=[(0, 0), (1, 0), (0, 1), (1, 1)],
)
TETRIS_S = TETROMINO(
    "tetris_s_0",
    center=(0, 0),
    color_ind="5",
    geometry=[(1, 0), (1, 1), (0, 1), (0, 2)],
)
TETRIS_T = TETROMINO(
    "tetris_t_0",
    center=(0, 0),
    color_ind="6",
    geometry=[(1, 0), (0, 1), (1, 1), (1, 2)],
)
TETRIS_Z = TETROMINO(
    "tetris_z_0",
    center=(0, 0),
    color_ind="7",
    geometry=[(0, 0), (0, 1), (1, 1), (1, 2)],
)

TETROMINOS = [
    TETRIS_I,
    TETRIS_J,
    TETRIS_L,
    TETRIS_O,
    TETRIS_S,
    TETRIS_T,
    TETRIS_Z,
]

LEFT_BOUND = 5
RIGHT_BOUND = 34
BOTTOM_BOUND = 69
TOP_BOUND = 10


class Tetris:
    def __init__(self, os):
        self.os = os
        self.current_bag = []
        self.refill_bag()
        self.current_piece = self.get_tetris_piece()
        self.current_piece.x = 17
        self.next_piece = self.get_tetris_piece()
        self.board = [["0"] * 10 for i in range(20)]
        self.i = 0
        self.game_over = False

    def step(self, keypressed):
        """
        Game event loop
        """
        if self.game_over:
            print("Game Over")
            return
        if self.i == 0:
            self.i = 0
            # print(self.board)
            score = self.os.get_score("tetris")
            self.os.blit("tetris_board", 0, 0)

            if keypressed[0]:  # hard drop
                pass
            elif keypressed[1]:  # left arrow key
                if self.current_piece.x > LEFT_BOUND:
                    print("Moving left")
                    self.current_piece.x = self.current_piece.x - 3

            elif keypressed[3]:  # right arrow key
                if self.current_piece.x < RIGHT_BOUND:
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

            if self.verify_and_check_intersection(
                self.current_piece
            ):  # check intersection and if it intersects then add it to the board!
                self.add_tetromino_to_board(self.current_piece)
                self.current_piece = self.next_piece
                self.current_piece.x = 17
                self.current_piece.y = TOP_BOUND
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
        if row_num < 0 or row_num >= len(self.board):
            return
        # remove the row
        del self.board[row_num]
        # insert an empty row at top
        self.board.insert(0, ["0"] * 10)

    def get_row_col_from_pixel(self, x, y):
        col = (x - LEFT_BOUND) // 3
        row = (y - TOP_BOUND) // 3
        return row, col

    def verify_and_check_intersection(
        self, tetromino
    ):  # checks if the piece at valid location and checks for intersection
        # check if even possible and in bounds!
        if (
            tetromino.y > BOTTOM_BOUND
            or tetromino.x < LEFT_BOUND
            or tetromino.x > RIGHT_BOUND
        ):
            return False

        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)

        for (
            row_offset,
            col_offset,
        ) in (
            tetromino.geometry
        ):  # because we are talking about intersection in the next step. we will
            print("row,col: ", row + row_offset + 1, col + col_offset)
            print("tetromino.geometry", tetromino.geometry)
            if (tetromino.y + 2) + (row_offset * 3) == BOTTOM_BOUND or self.board[
                row + row_offset + 1
            ][col + col_offset] != "0":
                return True
        return False

    def blit_board(self):
        for i in range(LEFT_BOUND, RIGHT_BOUND + 1, 3):
            for j in range(TOP_BOUND, BOTTOM_BOUND + 1, 3):
                row, col = self.get_row_col_from_pixel(i, j)
                if self.board[row][col] != "0":
                    self.os.blit("tetris_" + self.board[row][col], i, j)

    def add_tetromino_to_board(self, tetromino):
        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)
        for row_offset, col_offset in tetromino.geometry:
            self.board[row + row_offset][col + col_offset] = tetromino.color_ind

    def die(self):
        self.game_over = True
