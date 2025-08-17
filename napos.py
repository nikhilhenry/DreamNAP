from games import Menu, Aliens, Tetris, Demo


class NAPOperatingSystem:
    def __init__(self, driver):
        self.driver = driver
        self.selected_index = 1
        self.x_coord = 25
        self.current_scene = Menu(self)
        self.rgb_led = [(0, 0, 0)] * 5  # rgb

    def step(self, keypressed, gyro_data):
        """
        The main loop of the driver.
        """
        if keypressed[6]:  # go back to the menu when the home button is pressed
            self.change_scene("menu")
        self.current_scene.step(keypressed)
        self._show_led()

    def blit(self, asset_id, x, y):
        """
        Blit the asset on the display at the given coordinates.
        """
        self.driver.blit(asset_id, x, y)

    def clear_screen(self):
        self.driver.clear_screen()

    def display_num(self, number, x, y, align="left"):
        """
        Display the number on the screen.
        """
        if align == "left":
            for i, digit in enumerate(str(number)):
                if digit == ".":
                    self.driver.blit(
                        "dot",
                        x + i * 6,
                        y,
                    )
                else:
                    self.driver.blit(digit, x + i * 6, y)
        elif align == "right":
            for i, digit in enumerate(reversed(str(number))):
                if digit == ".":
                    self.driver.blit(
                        "dot",
                        x + i * 6,
                        y,
                    )
                else:
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

    def change_scene(self, scene_name):
        if scene_name == self.current_scene.__class__.__name__.lower():
            return
        if scene_name == "menu":
            self.current_scene = Menu(self)
        elif scene_name == "aliens":
            self.current_scene = Aliens(self)
        elif scene_name == "tetris":
            self.current_scene = Tetris(self)
        elif scene_name == "demo":
            self.current_scene = Demo(self)

        else:
            raise ValueError(f"Unknown scene: {scene_name}")

    def _show_led(self):
        for i, color in enumerate(self.rgb_led):
            self.driver.rgb_led[i] = (color[1], color[0], color[2])
        self.driver.rgb_led_show()

    def blit_battery(self, x, y):  # PRANJAL REPLACE THIS BRO THANSK!
        self.blit("battery_1by7", x, y)

    def get_voltage(self):
        return 3.1
