import pygame
import os
from config import ASSETS_DIR, SCREEN, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    """
    This class is handling properties and methods for Mac Gyver
    :returns  player
    """

    def __init__(self):
        """
        :rtype: object
        """
        pygame.sprite.Sprite.__init__(self)

        self.area = SCREEN.get_rect()
        self.speed = 10
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/player.png"))
        self.rect = self.image.get_rect()
        self.score = "0"
        self.collecting = False

    def moveup(self):
        if self.rect.y > 0:
            self.rect.y -= 25
            self.check_score()

    def movedown(self):
        if self.rect.y + 50 < HEIGHT:
            self.rect.y += 25
            self.check_score()

    def moveleft(self):
        if self.rect.x > 0:
            self.rect.x -= 25
            self.check_score()

    def moveright(self):
        if self.rect.x + 50 < WIDTH:
            self.rect.x += 25
            self.check_score()

    def check_score(self):
        return self.score

    def scoring_up(self):
        self.score = int(self.score)
        self.score += 1
        self.collecting = True
        return str(self.score)