class Menu:
    def __init__(self, os):
        self.os = os
        self.options = ["Option 1", "Option 2", "Option 3"]
        self.selected_index = 0
        self.os.store_score("aliens", 10)  # Initialize score storage

    def step(self, keypressed):
        """
        Game event loop
        """

        score = self.os.get_score("tetris")
        self.os.display_score(score, 5, 5)

        self.os.blit(
            "blue_square" if self.selected_index == 0 else "red_square", 25, 15
        )
        self.os.blit(
            "blue_square" if self.selected_index == 1 else "red_square", 25, 35
        )
        self.os.blit(
            "blue_square" if self.selected_index == 2 else "red_square", 25, 55
        )

        if keypressed[2]:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        if keypressed[0]:
            self.selected_index = (self.selected_index - 1) % len(self.options)
