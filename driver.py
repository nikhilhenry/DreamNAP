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
        }

        self.os = NAPOperatingSystem(self)

    def start(self):
        """
        The main loop of the driver.
        """

        self.running = True
        while self.running:

            keys_pressed = self.get_key_pressed_array()
            # clear the screen
            self.display.fill((0, 1, 0))
            self.os.step(keys_pressed, None)

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
