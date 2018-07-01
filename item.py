"""
Item Class : Where you can resize the ability of Mac Gyver to get Swiss Army Knives
"""
import os
import pygame
from config import ASSETS_DIR
from random import randint


class Item(pygame.sprite.Sprite):
    """
    This class is handling properties and methods for all kind of item
    :returns  any player without specialities
    """

    def __init__(self, pos, kind):
        pygame.sprite.Sprite.__init__(self)

        # Get the kind of the item is created
        self.kind = kind

        # Initialize the item
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx", kind+".png"))
        self.rect = pygame.Rect(pos[0], pos[1], 30, 30)

        # Change the orientation randomly
        self.random_orientation()

    def random_orientation(self):
        random_orientation = randint(0, 3)
        if random_orientation == 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif random_orientation == 1:
            self.image = pygame.transform.rotate(self.image, 180)
        elif random_orientation == 2:
            self.image = pygame.transform.rotate(self.image, 270)
