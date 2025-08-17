import pygame
from napos import NAPOperatingSystem


class Driver:
    """
    The class that handles rendering of the game using pygame.
    """

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((600, 905))
        self.display.fill((0, 1, 0))
        self.clock = pygame.time.Clock()

        self.asset_map = {
            "menu_aliens": pygame.image.load(
                "assets/menu/menu_aliens.png"
            ).convert_alpha(),
            "menu_tetris": pygame.image.load(
                "assets/menu/menu_tetris.png"
            ).convert_alpha(),
            "menu_demo": pygame.image.load("assets/menu/menu_demo.png").convert_alpha(),
            "0": pygame.image.load("assets/font_pack/0.png").convert_alpha(),
            "1": pygame.image.load("assets/font_pack/1.png").convert_alpha(),
            "2": pygame.image.load("assets/font_pack/2.png").convert_alpha(),
            "3": pygame.image.load("assets/font_pack/3.png").convert_alpha(),
            "4": pygame.image.load("assets/font_pack/4.png").convert_alpha(),
            "5": pygame.image.load("assets/font_pack/5.png").convert_alpha(),
            "6": pygame.image.load("assets/font_pack/6.png").convert_alpha(),
            "7": pygame.image.load("assets/font_pack/7.png").convert_alpha(),
            "8": pygame.image.load("assets/font_pack/8.png").convert_alpha(),
            "9": pygame.image.load("assets/font_pack/9.png").convert_alpha(),
            "load1": pygame.image.load("assets/utils/loading1.png").convert_alpha(),
            "load2": pygame.image.load("assets/utils/loading2.png").convert_alpha(),
            "load3": pygame.image.load("assets/utils/loading3.png").convert_alpha(),
            "load4": pygame.image.load("assets/utils/loading4.png").convert_alpha(),
            "load5": pygame.image.load("assets/utils/loading5.png").convert_alpha(),
            "load6": pygame.image.load("assets/utils/loading6.png").convert_alpha(),
            "load7": pygame.image.load("assets/utils/loading7.png").convert_alpha(),
            "load8": pygame.image.load("assets/utils/loading8.png").convert_alpha(),
            "load9": pygame.image.load("assets/utils/loading9.png").convert_alpha(),
            "load10": pygame.image.load("assets/utils/loading10.png").convert_alpha(),
            "playagain": pygame.image.load(
                "assets/utils/playagain.png"
            ).convert_alpha(),
            "battery_1by7": pygame.image.load(
                "assets/utils/battery_1by7.png"
            ).convert_alpha(),
            "battery_2by7": pygame.image.load(
                "assets/utils/battery_2by7.png"
            ).convert_alpha(),
            "battery_3by7": pygame.image.load(
                "assets/utils/battery_3by7.png"
            ).convert_alpha(),
            "battery_4by7": pygame.image.load(
                "assets/utils/battery_4by7.png"
            ).convert_alpha(),
            "battery_5by7": pygame.image.load(
                "assets/utils/battery_5by7.png"
            ).convert_alpha(),
            "battery_6by7": pygame.image.load(
                "assets/utils/battery_6by7.png"
            ).convert_alpha(),
            "battery_7by7": pygame.image.load(
                "assets/utils/battery_7by7.png"
            ).convert_alpha(),
            "heart_0by3": pygame.image.load("assets/utils/hearts0.png").convert_alpha(),
            "heart_1by3": pygame.image.load("assets/utils/hearts1.png").convert_alpha(),
            "heart_2by3": pygame.image.load("assets/utils/hearts2.png").convert_alpha(),
            "heart_3by3": pygame.image.load("assets/utils/hearts3.png").convert_alpha(),
            "alien_boss": pygame.image.load("assets/aliens/boss.png").convert_alpha(),
            "alien_cat": pygame.image.load("assets/aliens/cat.png").convert_alpha(),
            "alien_shield_1by3": pygame.image.load(
                "assets/aliens/shield_1by3.png"
            ).convert_alpha(),
            "alien_shield_2by3": pygame.image.load(
                "assets/aliens/shield_2by3.png"
            ).convert_alpha(),
            "alien_shield_3by3": pygame.image.load(
                "assets/aliens/shield_3by3.png"
            ).convert_alpha(),
            "alien_ship": pygame.image.load("assets/aliens/ship.png").convert_alpha(),
            "alien_ufo1": pygame.image.load("assets/aliens/ufo1.png").convert_alpha(),
            "alien_ufo2": pygame.image.load("assets/aliens/ufo2.png").convert_alpha(),
            "alien_ufo3": pygame.image.load("assets/aliens/ufo3.png").convert_alpha(),
            "alien_laser": pygame.image.load("assets/aliens/laser.png").convert_alpha(),
            "alien_over": pygame.image.load("assets/aliens/over.png").convert_alpha(),
            "tetris_1": pygame.image.load("assets/tetris/tetris_1.png").convert_alpha(),
            "tetris_2": pygame.image.load("assets/tetris/tetris_2.png").convert_alpha(),
            "tetris_3": pygame.image.load("assets/tetris/tetris_3.png").convert_alpha(),
            "tetris_4": pygame.image.load("assets/tetris/tetris_4.png").convert_alpha(),
            "tetris_5": pygame.image.load("assets/tetris/tetris_5.png").convert_alpha(),
            "tetris_6": pygame.image.load("assets/tetris/tetris_6.png").convert_alpha(),
            "tetris_7": pygame.image.load("assets/tetris/tetris_7.png").convert_alpha(),
            "tetris_i_0": pygame.image.load(
                "assets/tetris/tetris_i_0.png"
            ).convert_alpha(),
            "tetris_j_0": pygame.image.load(
                "assets/tetris/tetris_j_0.png"
            ).convert_alpha(),
            "tetris_l_0": pygame.image.load(
                "assets/tetris/tetris_l_0.png"
            ).convert_alpha(),
            "tetris_o_0": pygame.image.load(
                "assets/tetris/tetris_o_0.png"
            ).convert_alpha(),
            "tetris_s_0": pygame.image.load(
                "assets/tetris/tetris_s_0.png"
            ).convert_alpha(),
            "tetris_t_0": pygame.image.load(
                "assets/tetris/tetris_t_0.png"
            ).convert_alpha(),
            "tetris_z_0": pygame.image.load(
                "assets/tetris/tetris_z_0.png"
            ).convert_alpha(),
            "tetris_i_1": pygame.image.load(
                "assets/tetris/tetris_i_1.png"
            ).convert_alpha(),
            "tetris_j_1": pygame.image.load(
                "assets/tetris/tetris_j_1.png"
            ).convert_alpha(),
            "tetris_l_1": pygame.image.load(
                "assets/tetris/tetris_l_1.png"
            ).convert_alpha(),
            "tetris_o_1": pygame.image.load(
                "assets/tetris/tetris_o_1.png"
            ).convert_alpha(),
            "tetris_s_1": pygame.image.load(
                "assets/tetris/tetris_s_1.png"
            ).convert_alpha(),
            "tetris_t_1": pygame.image.load(
                "assets/tetris/tetris_t_1.png"
            ).convert_alpha(),
            "tetris_z_1": pygame.image.load(
                "assets/tetris/tetris_z_1.png"
            ).convert_alpha(),
            "tetris_i_2": pygame.image.load(
                "assets/tetris/tetris_i_2.png"
            ).convert_alpha(),
            "tetris_j_2": pygame.image.load(
                "assets/tetris/tetris_j_2.png"
            ).convert_alpha(),
            "tetris_l_2": pygame.image.load(
                "assets/tetris/tetris_l_2.png"
            ).convert_alpha(),
            "tetris_o_2": pygame.image.load(
                "assets/tetris/tetris_o_2.png"
            ).convert_alpha(),
            "tetris_s_2": pygame.image.load(
                "assets/tetris/tetris_s_2.png"
            ).convert_alpha(),
            "tetris_t_2": pygame.image.load(
                "assets/tetris/tetris_t_2.png"
            ).convert_alpha(),
            "tetris_z_2": pygame.image.load(
                "assets/tetris/tetris_z_2.png"
            ).convert_alpha(),
            "tetris_i_3": pygame.image.load(
                "assets/tetris/tetris_i_3.png"
            ).convert_alpha(),
            "tetris_j_3": pygame.image.load(
                "assets/tetris/tetris_j_3.png"
            ).convert_alpha(),
            "tetris_l_3": pygame.image.load(
                "assets/tetris/tetris_l_3.png"
            ).convert_alpha(),
            "tetris_o_3": pygame.image.load(
                "assets/tetris/tetris_o_3.png"
            ).convert_alpha(),
            "tetris_s_3": pygame.image.load(
                "assets/tetris/tetris_s_3.png"
            ).convert_alpha(),
            "tetris_t_3": pygame.image.load(
                "assets/tetris/tetris_t_3.png"
            ).convert_alpha(),
            "tetris_z_3": pygame.image.load(
                "assets/tetris/tetris_z_3.png"
            ).convert_alpha(),
            "tetris_board": pygame.image.load(
                "assets/tetris/tetris_board.png"
            ).convert_alpha(),
        }

        self.prev_keys_pressed = [0] * 7

        # LED strip state - 5 LEDs, each can be (R, G, B) or (0, 0, 0) for off
        self._led_states = [(0, 0, 0)] * 5
        self.rgb_led = [(0, 0, 0)] * 5

        self.os = NAPOperatingSystem(self)

    def start(self):
        """
        The main loop of the driver.
        """

        self.running = True
        while self.running:

            keys_pressed = self.get_key_pressed_array()
            keys_clicked = self.get_key_clicked_array(keys_pressed)

            # clear the screen
            # self.display.fill((0, 1, 0))
            self.os.step(keys_clicked, None)

            self._render_led_strip()

            self.prev_keys_pressed = keys_pressed.copy()

            pygame.display.flip()
            pygame.event.pump()
            self.clock.tick(60)

    def blit(self, asset_id, x, y):
        """
        Blit the asset on the display at the given coordinates.
        """
        asset = self.asset_map[asset_id]
        scaled_asset = pygame.transform.scale_by(asset, 10)
        self.display.blit(scaled_asset, (x * 10, y * 10))

    def get_key_pressed_array(self):
        keys = pygame.key.get_pressed()
        keys_pressed = [0] * 7
        if keys[pygame.K_UP]:
            keys_pressed[0] = 1
        if keys[pygame.K_LEFT]:
            keys_pressed[1] = 1
        if keys[pygame.K_DOWN]:
            keys_pressed[2] = 1
        if keys[pygame.K_RIGHT]:
            keys_pressed[3] = 1
        if keys[pygame.K_a]:
            keys_pressed[4] = 1
        if keys[pygame.K_s]:
            keys_pressed[5] = 1
        if keys[pygame.K_SPACE]:
            keys_pressed[6] = 1

        return keys_pressed

    def get_key_clicked_array(self, current_keys_pressed):
        """
        compare previous keypress state, click is detected when key transitions from 0 to 1.
        """
        keys_clicked = [0] * 7
        for i in range(7):
            if current_keys_pressed[i] == 1 and self.prev_keys_pressed[i] == 0:
                keys_clicked[i] = 1
        return keys_clicked

    def write_file(self, file_path, content):
        """
        Write byte array to a file.
        """
        complete_path = "./disk" + file_path
        with open(complete_path, "wb") as file:
            file.write(content)

    def read_file(self, file_path):
        """
        Read byte array from a file.
        """
        complete_path = "./disk" + file_path
        with open(complete_path, "rb") as file:
            return file.read()

    def clear_screen(self):
        """
        Clear the display.
        """
        self.display.fill((0, 1, 0))

    def rgb_led_show(self):
        """
        Show the RGB LED strip.
        """
        for i, color in enumerate(self.rgb_led):
            self._led_states[i] = (color[1], color[0], color[2])

    def _render_led_strip(self):
        """
        Render the LED strip at the bottom of the display as pixel art squares.
        """
        led_size = 80
        led_gap = 50
        strip_y = 815

        pygame.draw.rect(self.display, (100, 100, 100), (0, 800, 600, 5))

        for i in range(5):
            x = i * (led_size + led_gap)
            color = self._led_states[i]
            pygame.draw.rect(self.display, color, (x, strip_y, led_size, led_size))
