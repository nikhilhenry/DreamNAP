import pygame


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

    def start(self):
        """
        The main loop of the driver.
        """

        self.running = True
        while self.running:

            self.blit("red_square", 25, 35)
            self.blit("blue_square", 45, 35)
            pygame.display.flip()
            self.clock.tick(60)

    def blit(self, asset_id, x, y):
        """
        Blit the asset on the display at the given coordinates.
        """
        asset = self.asset_map[asset_id]
        scaled_asset = pygame.transform.scale_by(asset, 10)
        self.display.blit(scaled_asset, (x * 10, y * 10))
