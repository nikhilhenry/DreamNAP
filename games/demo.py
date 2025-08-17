class Demo:
    def __init__(self, os):
        self.os = os
        self.i = 0
        self.mode = 0
        self.led_offset = 0  # For scrolling animation
        self.led_timer = 0  # Timer for LED animation

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

    def step(self, keypressed):
        """
        Game event loop
        """
        self._update_led_animation()
        if keypressed[4]:
            self.mode = (self.mode + 1) % 3
            self.os.clear_screen()
            self.i = 0
        if self.mode == 0:  # LOADING & Music Demo
            self.os.blit(f"loading{self.i+1}", 0, 0)
            self.i += 1
            self.i = self.i % 10
        elif self.mode == 1:  # GYRO
            self.os.blit(f"ball", 30, 30)
        else:  # Battery Demo
            self.os.blit_battery(20, 30)
            self.os.display_num(self.os.get_voltage(), 30, 40, align="left")
            self.i += 1
            self.i = self.i % 7
