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

    def display_score(self, score, x, y, align="left"):
        """
        Display the score on the screen.
        """
        if align == "left":
            for i, digit in enumerate(str(score)):
                self.driver.blit(digit, x + i * 6, y)
        elif align == "right":
            for i, digit in enumerate(reversed(str(score))):
                self.driver.blit(digit, x - i * 6, y)

    def store_score(self, game, score):
        current_content = self.driver.read_file("/high_scores.txt").decode()
        current_scores = current_content.splitlines()
        current_scores = [
            line for line in current_scores if not line.startswith(f"{game}:")
        ]
        current_scores.append(f"{game}:{score}")
        self.driver.write_file("/high_scores.txt", "\n".join(current_scores).encode())

    def get_score(self, game):
        try:
            for line in self.driver.read_file("/high_scores.txt").decode().splitlines():
                if line.startswith(f"{game}:"):
                    return int(line.split(":")[1])
            return 0
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0
