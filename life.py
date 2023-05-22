import pygame
import random


from player import SCREEN_WIDTH, SCREEN_HEIGHT

class LifeEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(LifeEnemy, self).__init__()
        self.surf = pygame.image.load("src/jet.png").convert_alpha()
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH + 20, random.randint(100, SCREEN_HEIGHT - 100))
        )
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
