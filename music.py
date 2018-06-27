import pygame
import os
from config import ASSETS_DIR


class Music:
    """
    This class is made to get a cleaner code when handling music
    """

    def __init__(self, music_status=1):
        self.music = pygame.mixer.music.load(os.path.join(ASSETS_DIR, "sfx/music.mp3"))
        self.play_img = pygame.image.load(os.path.join(ASSETS_DIR, 'gfx/play_music.png'))
        self.stop_img = pygame.image.load(os.path.join(ASSETS_DIR, 'gfx/stop_music.png'))
        self.is_playing = False

    def play(self):
        # args : Number of loops (-1 is an infinite loop)
        pygame.mixer.music.play(-1)
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()

    def fadeout(self):
        pygame.mixer.music.fadeout(4000)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
