class Menu:
    def __init__(self, os):
        self.os = os
        self.selected_index = 0

        self.options = {
            0: "tetris",
            1: "aliens",
            2: "demo",
        }

    def step(self, keypressed):
        """
        Game event loop
        """

        score = self.os.get_score(self.options[self.selected_index])

        self.os.blit(f"menu_{self.options[self.selected_index]}", 0, 0)
        self.os.display_score(score, 45, 66, align="right")

        if keypressed[3]:
            self.selected_index += 1
        if keypressed[1]:
            self.selected_index -= 1
        self.selected_index = max(0, min(self.selected_index, len(self.options) - 1))
