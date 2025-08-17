import random

LEFT_BOUND = 5
RIGHT_BOUND = 33
BOTTOM_BOUND = 75
TOP_BOUND = 17
MIDDLE_POS = (RIGHT_BOUND - LEFT_BOUND - 1) // 2
START_POS = TOP_BOUND - 15


class TETROMINO:
    def __init__(self, name, color_ind, geometries):
        self.name = name
        self.initial_rot = 0
        self.color_ind = color_ind
        self.x = 46
        self.y = TOP_BOUND + 5
        self.geometries = geometries  # geometry for all the rotations
        self.geometry = geometries[0]

    def rotate_left(self):
        self.initial_rot = (self.initial_rot - 1) % 4
        self.geometry = self.geometries[self.initial_rot]
        self.name = self.name[:-1] + str(self.initial_rot)

    def rotate_right(self):
        self.initial_rot = (self.initial_rot + 1) % 4
        self.geometry = self.geometries[self.initial_rot]
        self.name = self.name[:-1] + str(self.initial_rot)


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
        self.current_piece.x = MIDDLE_POS
        self.current_piece.y = START_POS
        self.next_piece = self.get_tetris_piece()
        self.board = [["0"] * 10 for _ in range(20)]
        self.game_over = False
        self.i = 0
        self.score = 0
        self.led_offset = 0  # For scrolling animation
        self.led_timer = 0  # Timer for LED animation

    def _set_leds(self, color, duration=5):
        """Helper to set all LEDs to a solid color for a short duration"""
        for i in range(5):
            self.os.rgb_led[i] = color
        self.led_timer = -duration  # negative timer pauses animation temporarily

    def _blink_leds(self, color, times=5000, interval=5):
        """Blink all LEDs a few times with given color"""
        self.blink_color = color
        self.blink_times = times * 2  # on/off counts
        self.blink_interval = interval
        self.blink_counter = 0
        self.led_timer = -1  # stop normal animation during blink

    def _update_blink(self):
        """Handle blink animation if active"""
        if hasattr(self, "blink_times") and self.blink_times > 0:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_interval:
                self.blink_counter = 0
                self.blink_times -= 1
                # toggle LEDs
                if self.blink_times % 2 == 0:
                    for i in range(5):
                        self.os.rgb_led[i] = self.blink_color  # red
                else:
                    for i in range(5):
                        self.os.rgb_led[i] = (255, 255, 255)  # white
            return True
        return False

    def _update_led_animation(self):
        """
        Master LED animation update (handles blinking or color cycle).
        """
        if self._update_blink():
            return  # blinking overrides normal animation

        # normal rainbow cycle
        colors = [
            (44, 232, 244),  # blue
            (180, 0, 255),  # purple
            (255, 0, 0),  # red
            (255, 165, 0),  # orange
            (255, 255, 0),  # yellow
            (0, 255, 0),  # green
        ]

        self.led_timer += 1
        if self.led_timer >= 10:
            self.led_timer = 0
            self.led_offset = (self.led_offset - 1) % (len(colors) * 5)

        for i in range(5):
            pattern_position = (i + self.led_offset) % (len(colors) * 5)
            color_index = pattern_position // 5
            self.os.rgb_led[i] = colors[color_index]

    def step(self, keypressed):
        """
        Game event loop
        """
        if self.game_over:
            print("Game Over")
            self.os.clear_screen()
            self._update_led_animation()
            self.os.blit("alien_over", 25, 35)
            return

        # Track the most recent single key pressed
        key_id = None
        for i, pressed in enumerate(keypressed):
            if pressed:
                key_id = i  # overwrite → ensures "last pressed before tick"
        if key_id is not None:
            self.keybuffer = key_id

        if self.i == 0:
            self._update_led_animation()
            self.i = 0
            highscore = self.os.get_score("tetris")
            if self.score > highscore:
                self.os.store_score("tetris", self.score)
                highscore = self.score
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
                    + (
                        (
                            max(
                                [
                                    col_offset
                                    for row_offset, col_offset in self.current_piece.geometry
                                ]
                            )
                            + 1
                        )
                        * 3
                    )
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
                self.current_piece.x = MIDDLE_POS
                self.current_piece.y = START_POS
                self.next_piece = self.get_tetris_piece()
            else:
                self.os.blit(
                    self.current_piece.name, self.current_piece.x, self.current_piece.y
                )

            self.os.blit(self.next_piece.name, self.next_piece.x, self.next_piece.y)
            self.os.display_num(highscore, 51, 45, align="right")  # highscore
            self.os.display_num(self.score, 51, 68, align="right")  # score
            self.blit_board()

            self.keybuffer = None

        else:
            self.i += 1

    def can_rotate(self, tetromino, new_geometry):
        """Check if rotating into new_geometry is valid (no collisions or out-of-bounds)."""
        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)

        for (
            row_offset,
            col_offset,
        ) in new_geometry:  # check this for a future row instead # TODO
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
        cleared = False
        for r in range(len(self.board)):
            if all(cell != "0" for cell in self.board[r]):
                self.score += 10
                self.clear_row(r)
                cleared = True
        if cleared:
            # flash orange when clearing line(s)
            orange = (255, 165, 0)
            self._set_leds(orange, duration=10)

    def get_row_col_from_pixel(self, x, y):
        col = (x - LEFT_BOUND + 1) // 3
        row = (y - TOP_BOUND) // 3
        return row, col

    def verify_and_check_intersection(self, tetromino):
        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)

        for row_offset, col_offset in tetromino.geometry:
            r = row + row_offset
            c = col + col_offset

            # bottom collision
            if r + 1 >= len(self.board):
                return True

            # block collision
            if (r == 0 or r == -1) and self.board[r + 1][c] != "0":
                self.die()
                return False
            if r >= 0 and self.board[r + 1][c] != "0":
                return True
        return False

    def blit_board(self):
        for i in range(LEFT_BOUND, RIGHT_BOUND + 1, 3):
            for j in range(TOP_BOUND, BOTTOM_BOUND + 1, 3):
                row, col = self.get_row_col_from_pixel(i, j)
                if self.board[row][col] != "0":
                    self.os.blit("tetris_" + self.board[row][col], i - 1, j - 1)

    def add_tetromino_to_board(self, tetromino):
        row, col = self.get_row_col_from_pixel(tetromino.x, tetromino.y)
        for row_offset, col_offset in tetromino.geometry:
            self.board[row + row_offset][col + col_offset] = tetromino.color_ind

    def die(self):
        self.game_over = True
        self.led_timer = 0  # reset so blink starts clean

        # blink red ↔ white
        self._blink_leds((255, 0, 0), times=10, interval=5)
