import random


class Aliens:
    def __init__(self, os):
        self.os = os
        self.selected_index = 0
        self.shield_state = [3, 3, 3]
        self.player_health = 3
        self.os.clear_screen()
        self.player_pos = 25
        self.aliens = []
        """
        all lasers: [x, y, type] where type is 'player' or 'alien'
        """
        self.lasers = []
        self.alien_spawn_timer = 0
        self.alien_shoot_timer = 0
        self.score = 0
        self.game_over = False

    def step(self, keypressed):
        """
        Game event loop
        """

        # check for game over
        if self.game_over:
            self.os.clear_screen()
            self._draw_game_over()
            if keypressed[6]:  # home button to return to menu
                self.os.change_scene("menu")
            return

        self.os.clear_screen()
        self._draw_statsbar()
        self._draw_shields()
        self.os.blit("alien_ship", self.player_pos, 69)

        if keypressed[1]:
            self.player_pos -= 1
        if keypressed[3]:
            self.player_pos += 1
        if keypressed[4]:
            # fire laser
            self.lasers.append([self.player_pos + 7, 67, "player"])

        self.player_pos = max(5, min(self.player_pos, 45))

        self.alien_spawn_timer += 1
        if self.alien_spawn_timer % 40 == 0 and len(self.aliens) < 3:
            alien_x = random.randint(5, 45)
            self.aliens.append([alien_x, 10])

        for alien in self.aliens:
            self.os.blit("alien_ufo1", alien[0], alien[1])

        # aliens shoot lasers periodically
        self.alien_shoot_timer += 1
        if self.alien_shoot_timer % 60 == 0 and len(self.aliens) > 0:
            # random alien shoots
            shooting_alien = random.choice(self.aliens)
            self.lasers.append([shooting_alien[0] + 7, shooting_alien[1] + 10, "alien"])

        for laser in self.lasers:
            if laser[2] == "player":
                laser[1] -= 3
            elif laser[2] == "alien":
                laser[1] += 2

        for laser in self.lasers:
            self.os.blit("alien_laser", laser[0], laser[1])

        """
        collision check
        """
        destroyed_aliens = []
        destroyed_lasers = []
        for i, alien in enumerate(self.aliens):
            for j, laser in enumerate(self.lasers):
                if (
                    laser[2] == "player"
                    and abs(alien[0] - laser[0]) < 10
                    and abs(alien[1] - laser[1]) < 10
                ):
                    destroyed_aliens.append(i)
                    destroyed_lasers.append(j)
                    self.score += 1

        # remove destroyed aliens and lasers
        self.aliens = [
            a for idx, a in enumerate(self.aliens) if idx not in destroyed_aliens
        ]
        self.lasers = [
            l for idx, l in enumerate(self.lasers) if idx not in destroyed_lasers
        ]

        # check shield collisions and player hits
        remaining_lasers = []
        for laser in self.lasers:
            laser_removed = False

            # shield collision (only alien lasers damage shields)
            if laser[2] == "alien":
                for i, shield_state in enumerate(self.shield_state):
                    if shield_state > 0:
                        shield_x = 5 + i * 20
                        shield_y = 60
                        if (
                            abs(laser[0] - (shield_x + 7)) < 10
                            and abs(laser[1] - shield_y) < 8
                        ):
                            self.shield_state[i] -= 1
                            laser_removed = True
                            break

            if not laser_removed:
                # bounds check and player collision
                if laser[2] == "player" and laser[1] > 0:
                    remaining_lasers.append(laser)
                elif laser[2] == "alien" and laser[1] < 70:
                    # Check if alien laser hits player
                    if (
                        abs(laser[0] - (self.player_pos + 7)) < 8
                        and abs(laser[1] - 69) < 5
                    ):
                        # Player hit! Reduce health
                        self.player_health -= 1
                        if self.player_health <= 0:
                            self.game_over = True
                    else:
                        remaining_lasers.append(laser)

        self.lasers = remaining_lasers
        self.os.store_score("aliens", self.score)

    def _draw_statsbar(self):
        score = self.score
        self.os.display_num(score, 55, 1, align="right")
        self.os.blit("battery_3by7", 1, 1)
        if self.player_health >= 0:
            self.os.blit(f"heart_{self.player_health}by3", 21, 1)

    def _draw_shields(self):
        for i, state in enumerate(self.shield_state):
            if state:
                self.os.blit(f"alien_shield_{state}by3", 5 + i * 20, 60)

    def _draw_game_over(self):
        """Draw game over screen"""
        self.os.display_num(self.score, 25, 30, align="left")
        self.os.blit("heart_0by3", 21, 40)
