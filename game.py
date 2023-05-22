class Game:
    def __init__(self):
        self.score = 0
        self.life = 3
        self.game_over = False

    def increase_score(self, delta_score):
        self.score += delta_score

    def reduce_life(self):
        self.life -= 1

    def is_game_over(self):
        if self.life <= 0:
            self.game_over = True
        return self.game_over

    def get_score(self):
        return self.score

    def get_life(self):
        return self.life

    def set_game_over(self):
        self.game_over = True

    def quit_game(self):
        pygame.quit()
