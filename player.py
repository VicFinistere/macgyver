import pygame
import os
from config import ASSETS_DIR, SCREEN, WIDTH, HEIGHT

class Player(pygame.sprite.Sprite):
    """
    This class is handling properties and methods for Mac Gyver
    :returns  player
    """

    def __init__(self, pos):
        """
        :rtype: object
        """
        pygame.sprite.Sprite.__init__(self)

        self.area = SCREEN.get_rect()
        self.speed = 16
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/player.png"))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(pos[0]*32, pos[1]*32, 32, 32)
        self.score = "0"
        self.collecting = False

    def moveup(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed

    def movedown(self):
        if self.rect.y + self.speed*2 < HEIGHT:
            self.rect.y += self.speed

    def moveleft(self):
        if self.rect.x > 0:
            self.rect.x -= self.speed

    def moveright(self):
        if self.rect.x + self.speed*2 < WIDTH:
            self.rect.x += self.speed

    def check_score(self):
        return self.score

    def scoring_up(self):
        self.score = int(self.score)
        self.score += 1
        self.collecting = True
        return str(self.score)