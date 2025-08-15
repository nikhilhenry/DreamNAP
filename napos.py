from games import Menu


class NAPOperatingSystem:
    def __init__(self, driver):
        self.driver = driver
        self.selected_index = 1
        self.x_coord = 25
        self.menu = Menu(self)

    def step(self, keypressed, gyro_data):
        """
        The main loop of the driver.
        """
        self.menu.step(keypressed)

    def blit(self, asset_id, x, y):
        """
        Blit the asset on the display at the given coordinates.
        """
        self.driver.blit(asset_id, x, y)

    def display_score(self, score, x, y):
        """
        Display the score on the screen.
        """
        for i, digit in enumerate(str(score)):
            self.driver.blit(digit, x + i * 6, y)

    def store_score(self, score):
        self.driver.write_file("/high_scores.txt", str(score).encode())
    def get_score(self):
        try:
            return int(self.driver.read_file("/high_scores.txt").decode())
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0