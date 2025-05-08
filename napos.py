class NAPOperatingSystem:
    def __init__(self, driver):
        self.driver = driver
        self.y_coord = 5

    def step(self,keypressed,gyro_data):
        """
        The main loop of the driver.
        """
        self.driver.blit("blue_square", 5, self.y_coord)
        self.driver.blit("red_square", 25, self.y_coord)
        self.driver.blit("blue_square", 45, self.y_coord)

        if keypressed[2]:
            self.y_coord += 1
        if keypressed[0]:
            self.y_coord -= 1
