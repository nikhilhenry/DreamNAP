class NAPOperatingSystem:
    def __init__(self, driver):
        self.driver = driver
        self.selected_index = 1
        self.x_coord = 25 

    def step(self,keypressed,gyro_data):
        """
        The main loop of the driver.
        """
        self.driver.blit("blue_square" if self.selected_index == 0 else "red_square", self.x_coord,15)
        self.driver.blit("blue_square" if self.selected_index == 1 else "red_square", self.x_coord,35)
        self.driver.blit("blue_square" if self.selected_index == 2 else "red_square",self.x_coord,55)

        if keypressed[2]:
            self.selected_index += 1 
        if keypressed[0]:
            self.selected_index -= 1
        self.selected_index %= 3