import pygame
import os
from pygame.locals import *
from config import SCREEN, ASSETS_DIR, COLORS, HEIGHT, WIDTH


class Intro:
    """
    Introduction Scene
    """
    def __init__(self):

        # Text fonts
        font = pygame.font.Font(None, 42)
        inst_font = pygame.font.Font(None, 24)

        # Texts
        text_content = "Mac Gyver Maze"
        inst_content = "( Press a key or click to play)"

        # Title element
        self.title = font.render(text_content, 1, (COLORS["WHITE"]))
        self.title_rect = (font.size(text_content))[0]

        # Instructions element
        self.inst = inst_font.render(inst_content, 1, (COLORS["WHITE"]))
        self.inst_rect = (inst_font.size(inst_content))[0]

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
        background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/splashscreen.png"))
        SCREEN.blit(background, (0, 0))
        # Blit everything to the screen
        SCREEN.blit(self.title, ((WIDTH - self.title_rect)/2, HEIGHT / 2))
        SCREEN.blit(self.inst, ((WIDTH - self.title_rect)/2, HEIGHT - 50))
        pygame.display.flip()
        pygame.time.wait(500)
        self.update()
