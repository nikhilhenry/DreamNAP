import random


class TETROMINO:
    def __init__(self, name, center, color_ind, geometries):
        self.name = name
        self.initial_rot = 0
        self.center = center
        self.color_ind = color_ind
        self.x = 45 + center[0]
        self.y = 14 + center[1]
        self.geometries = geometries  # list of 4 geometries
        self.geometry = geometries[0]

    def rotate_left(self):
        self.initial_rot = (self.initial_rot - 1) % 4
        self.geometry = self.geometries[self.initial_rot]
        self.name = self.name[:-1] + str(self.initial_rot)

    def rotate_right(self):
        self.initial_rot = (self.initial_rot + 1) % 4
        self.geometry = self.geometries[self.initial_rot]
        self.name = self.name[:-1] + str(self.initial_rot)


LEFT_BOUND = 5
RIGHT_BOUND = 34
BOTTOM_BOUND = 69
TOP_BOUND = 10


def shuffle(lst):
    n = len(lst)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)  # pick random index in [0, i]
        lst[i], lst[j] = lst[j], lst[i]


class Tetris:
    def __init__(self, os):
        self.os = os
        self.current_bag = []
        self.refill_bag()
        self.current_piece = self.get_tetris_piece()
        self.current_piece.x = 17
        self.current_piece.y = TOP_BOUND
        self.next_piece = self.get_tetris_piece()
        self.board = [["0"] * 10 for _ in range(20)]
        self.game_over = False
        self.i = 0

    def step(self, keypressed):
        """
        Game event loop
        """
        if self.game_over:
            print("Game Over")
            return

        # Track the most recent single key pressed
        key_id = None
        for i, pressed in enumerate(keypressed):
            if pressed:
                key_id = i  # overwrite → ensures "last pressed before tick"
        if key_id is not None:
            self.keybuffer = key_id

        if self.i == 6:
            self.i = 0
            score = self.os.get_score("tetris")
            self.os.blit("tetris_board", 0, 0)

            # Use the buffered key (if any)
            k = getattr(self, "keybuffer", None)

            if k == 0:  # hard drop
                pass
            elif k == 1:  # left arrow
                if self.current_piece.x > LEFT_BOUND:
                    print("Moving left")
                    self.current_piece.x -= 3
            elif k == 3:  # right arrow
                if (
                    self.current_piece.x
                    + (max([x for x, y in self.current_piece.geometry]) * 3)
                    + 1
                    < RIGHT_BOUND
                ):
                    print("Moving right")
                    self.current_piece.x += 3
            elif k == 4:  # rotate anticlockwise
                print("Rotate anticlockwise")
                self.try_rotate_left()
            elif k == 5:  # rotate clockwise
                print("Rotate clockwise")
                self.try_rotate_right()

            # Always move down
            if k == 2:  # soft drop
                print("Going Fast!")
                self.current_piece.y += 1
            self.current_piece.y += 1

            if self.verify_and_check_intersection(self.current_piece):
                self.add_tetromino_to_board(self.current_piece)
                self.clear_full_rows()
                self.current_piece = self.next_piece
                self.current_piece.x = 17
                self.current_piece.y = TOP_BOUND
                self.next_piece = self.get_tetris_piece()
            else:
                self.os.blit(
                    self.current_piece.name, self.current_piece.x, self.current_piece.y
                )

            self.os.blit(self.next_piece.name, self.next_piece.x, self.next_piece.y)
            self.os.display_num(score, 48, 39, align="right")
            self.blit_board()

            self.keybuffer = None

        else:
            self.i += 1

    def can_rotate(self, tetromino, new_geometry):
        """Check if rotating into new_geometry is valid (no collisions or out-of-bounds)."""
        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)

        for row_offset, col_offset in new_geometry:
            # Compute absolute position
            r = row + row_offset
            c = col + col_offset

            # Bounds check
            if r < 0 or r >= len(self.board) or c < 0 or c >= len(self.board[0]):
                return False

            # Collision check
            if self.board[r][c] != "0":
                return False
        return True

    def try_rotate_left(self):
        """Rotate left only if safe"""
        next_rot = (self.current_piece.initial_rot - 1) % 4
        new_geometry = self.current_piece.geometries[next_rot]

        if self.can_rotate(self.current_piece, new_geometry):
            self.current_piece.rotate_left()

    def try_rotate_right(self):
        """Rotate right only if safe"""
        next_rot = (self.current_piece.initial_rot + 1) % 4
        new_geometry = self.current_piece.geometries[next_rot]

        if self.can_rotate(self.current_piece, new_geometry):
            self.current_piece.rotate_right()

    def refill_bag(self):
        self.current_bag.extend(
            [
                TETROMINO(
                    "tetris_i_0",
                    center=(0, 0),
                    color_ind="1",
                    geometries=[
                        [(0, 0), (1, 0), (2, 0), (3, 0)],
                        [(0, 0), (0, 1), (0, 2), (0, 3)],
                        [(0, 0), (1, 0), (2, 0), (3, 0)],
                        [(0, 0), (0, 1), (0, 2), (0, 3)],
                    ],
                ),
                TETROMINO(
                    "tetris_j_0",
                    center=(0, 0),
                    color_ind="2",
                    geometries=[
                        [(0, 1), (1, 1), (2, 1), (2, 0)],
                        [(0, 0), (1, 0), (1, 1), (1, 2)],
                        [(0, 0), (0, 1), (1, 0), (2, 0)],
                        [(0, 0), (0, 1), (0, 2), (1, 2)],
                    ],
                ),
                TETROMINO(
                    "tetris_l_0",
                    center=(0, 0),
                    color_ind="3",
                    geometries=[
                        [(0, 0), (1, 0), (2, 0), (2, 1)],
                        [(0, 0), (0, 1), (0, 2), (1, 0)],
                        [(0, 0), (0, 1), (1, 1), (2, 1)],
                        [(0, 2), (1, 0), (1, 1), (1, 2)],
                    ],
                ),
                TETROMINO(
                    "tetris_o_0",
                    center=(0, 0),
                    color_ind="4",
                    geometries=[
                        [(0, 0), (1, 0), (0, 1), (1, 1)],
                        [(0, 0), (1, 0), (0, 1), (1, 1)],
                        [(0, 0), (1, 0), (0, 1), (1, 1)],
                        [(0, 0), (1, 0), (0, 1), (1, 1)],
                    ],
                ),
                TETROMINO(
                    "tetris_s_0",
                    center=(0, 0),
                    color_ind="5",
                    geometries=[
                        [(1, 0), (1, 1), (0, 1), (0, 2)],
                        [(0, 0), (1, 0), (1, 1), (2, 1)],
                        [(1, 0), (1, 1), (0, 1), (0, 2)],
                        [(0, 0), (1, 0), (1, 1), (2, 1)],
                    ],
                ),
                TETROMINO(
                    "tetris_t_0",
                    center=(0, 0),
                    color_ind="6",
                    geometries=[
                        [(1, 0), (0, 1), (1, 1), (1, 2)],
                        [(0, 0), (1, 0), (1, 1), (2, 0)],
                        [(0, 0), (0, 1), (0, 2), (1, 1)],
                        [(0, 1), (1, 0), (1, 1), (2, 1)],
                    ],
                ),
                TETROMINO(
                    "tetris_z_0",
                    center=(0, 0),
                    color_ind="7",
                    geometries=[
                        [(0, 0), (0, 1), (1, 1), (1, 2)],
                        [(0, 1), (1, 0), (1, 1), (2, 0)],
                        [(0, 0), (0, 1), (1, 1), (1, 2)],
                        [(0, 1), (1, 0), (1, 1), (2, 0)],
                    ],
                ),
            ]
        )
        shuffle(self.current_bag)

    def get_tetris_piece(self):
        if len(self.current_bag) == 0:
            self.refill_bag()
        return self.current_bag.pop(0)

    def clear_row(self, row_num):
        if 0 <= row_num < len(self.board):
            del self.board[row_num]
            self.board.insert(0, ["0"] * 10)

    def clear_full_rows(self):
        for r in range(len(self.board)):
            if all(cell != "0" for cell in self.board[r]):
                self.clear_row(r)

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
            if (
                self.board[row + row_offset][col + col_offset] != "0"
            ):  # this is wrong as it is still incomplete! check all geometry because return yes.
                self.die()
                return False
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
