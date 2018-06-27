import os
import pygame
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
        """
        Play the music
        :return: (bool) music status ( True / False )
        """
        # args : Number of loops (-1 is an infinite loop)
        pygame.mixer.music.play(-1)
        self.is_playing = True

    def stop(self):
        """
        Stop the music ( easier to read in code )
        """
        pygame.mixer.music.stop()

    def fadeout(self):
        """
        Fadeout the music ( easier to read in code )
        """
        pygame.mixer.music.fadeout(4000)

    def pause(self):
        """
        Pause the music(easier to read in code )
        """
        pygame.mixer.music.pause()

    def unpause(self):
        """
        Stop the music pause ( easier to read in code )
        """
        pygame.mixer.music.unpause()
