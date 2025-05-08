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
        self.running = True
        self.red_square = pygame.image.load("assets/red_square.bmp").convert()
        self.red_square = pygame.transform.scale_by(self.red_square, 10)

    def step(self):
        """
        The main loop of the game.
        """
        while self.running:

            self.blit("red_square", 25, 35)
            pygame.display.flip()
            self.clock.tick(60)
    
    def blit(self,asset_id, x, y):
        """
        Blit the asset on the display at the given coordinates.
        """

        self.display.blit(self.red_square, (x*10, y*10))