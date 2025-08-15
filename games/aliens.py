class Aliens:
    def __init__(self, os):
        self.os = os
        self.selected_index = 0

    def step(self, keypressed):
        """
        Game event loop
        """

        score = self.os.get_score("aliens")

        self.os.display_score(score, 45, 66, align="right")
