import pygame
from pygame.locals import *

import config


class Intro:
    """
    Introduction Scene
    """
    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render("Mac Gyver Maze", 1, (config.COLORS["WHITE"]))

        # Launching
        self.run = True
        self.state = 0
        self.draw()

    def update(self):
        """
        Event loop
        """
        while self.run:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    self.state = 1
                    self.run = False
                elif event.type == QUIT:
                    self.run = False
            pygame.time.wait(500)
            self.draw()
        return self.state

    def draw(self):
        """
        Fill background and blit everything to the screen
        """
        # Fill background
        config.SCREEN.fill(config.COLORS["BLACK"])

        # Blit everything to the screen
        config.SCREEN.blit(self.text, (160, config.HEIGHT / 2))
        pygame.display.flip()
        pygame.time.wait(500)
        self.update()
