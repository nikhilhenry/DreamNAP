import pygame
from napos import NAPOperatingSystem


class Driver:
    """
    The class that handles rendering of the game using pygame.
    """

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((600, 800))
        self.display.fill((0, 1, 0))
        self.clock = pygame.time.Clock()

        self.asset_map = {
            "red_square": pygame.image.load("assets/red_square.bmp").convert(),
            "blue_square": pygame.image.load("assets/blue_square.bmp").convert(),
            "blue_square": pygame.image.load("assets/blue_square.bmp").convert(),
            "0": pygame.image.load("assets/0.png").convert_alpha(),
            "1": pygame.image.load("assets/1.png").convert_alpha(),
            "2": pygame.image.load("assets/2.png").convert_alpha(),
            "3": pygame.image.load("assets/3.png").convert_alpha(),
            "4": pygame.image.load("assets/4.png").convert_alpha(),
            "5": pygame.image.load("assets/5.png").convert_alpha(),
            "6": pygame.image.load("assets/6.png").convert_alpha(),
            "7": pygame.image.load("assets/7.png").convert_alpha(),
            "8": pygame.image.load("assets/8.png").convert_alpha(),
            "9": pygame.image.load("assets/9.png").convert_alpha(),
        }

        self.prev_keys_pressed = [0] * 7

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
            self.display.fill((0, 1, 0))
            self.os.step(keys_clicked, None)

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
        with open(complete_path, 'wb') as file:
            file.write(content)
    
    def read_file(self, file_path):
        """
        Read byte array from a file.
        """
        complete_path = "./disk" + file_path
        with open(complete_path, 'rb') as file:
            return file.read()
