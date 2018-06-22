import pygame
import os
from config import ASSETS_DIR


class Music:
    """
    This class is made to get a cleaner code when handling music
    """
    def __init__(self):
        self.music = pygame.mixer.music.load(os.path.join(ASSETS_DIR, "sfx/music.mp3"))

    def play(self):
        # args : Number of loops (-1 is an infinite loop)
        pygame.mixer.music.play(-1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def fadeout(self):
        pygame.mixer.music.fadeout(4000)
