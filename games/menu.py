class Menu:
    def __init__(self, os):
        self.os = os
        self.selected_index = 0
        self.led_offset = 0  # For scrolling animation
        self.led_timer = 0  # Timer for LED animation

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
        self.os.display_num(score, 45, 66, align="right")

        # Update LED scrolling animation
        self._update_led_animation()

        if keypressed[3]:
            self.selected_index += 1
        if keypressed[1]:
            self.selected_index -= 1
        if keypressed[4]:
            self.os.change_scene(self.options[self.selected_index])
        self.selected_index = max(0, min(self.selected_index, len(self.options) - 1))

    def _update_led_animation(self):
        """
        Update LED animation with scrolling half blue and half white pattern
        """
        self.led_timer += 1
        if self.led_timer >= 10:
            self.led_timer = 0
            self.led_offset = (self.led_offset - 1) % 10

        blue = (44, 232, 244)
        white = (255, 255, 255)

        for i in range(5):
            pattern_position = (i + self.led_offset) % 10
            if pattern_position < 5:
                self.os.rgb_led[i] = white
            else:
                self.os.rgb_led[i] = blue
