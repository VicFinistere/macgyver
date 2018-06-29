import os
import pygame
from config import ASSETS_DIR


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

        self.speed = 32
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/player.png"))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Rect(pos[0] * 32, pos[1] * 32, 32, 32)
        self.score = "0"
        self.collecting = False

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def scoring_up(self):
        self.score = int(self.score)
        self.score += 1
        self.collecting = True
        return str(self.score)
