import pygame
import os
from pygame.locals import *

from config import ASSETS_DIR, COLORS, SCREEN, WIDTH, HEIGHT

class End:
    def __init__(self):

        # Text fonts
        font = pygame.font.Font(None, 48)
        inst_font = pygame.font.Font(None, 24)

        # Texts
        text_content = "The end"
        inst_content = "(Click again to quit)"

        # Score from file
        score_file = open("score.txt", "r")
        score_content = score_file.read()
        score_file.close()

        # Pygame Texts Elements
        self.inst = inst_font.render(inst_content, 1, (COLORS["WHITE"]))
        self.inst_rect = (inst_font.size(inst_content))[0]
        self.text = font.render(text_content, 1, (COLORS["WHITE"]))
        self.text_rect = (font.size(text_content))[0]


        # Victory Message
        self.score = inst_font.render(score_content, 1, (COLORS["WHITE"]))
        self.score_rect = (inst_font.size(score_content))[0]

        # Launching
        self.run = True
        self.draw()

    def update(self):
        """
        Event loop with quit abilities
        """
        while self.run:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN or event.type == QUIT:
                    self.run = False
            pygame.time.wait(500)
            self.draw()

    def draw(self):
        """
        Fill background and blit everything to the screen
        """
        # Fill background
        background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/splashscreen.png"))
        SCREEN.blit(background, (0, 0))

        # VICTORY CASE
        SCREEN.blit(self.score, ((WIDTH / 2) - (self.score_rect / 2), HEIGHT - 20))

        # Blit everything to the screen
        SCREEN.blit(self.text, ((WIDTH / 2) - (self.text_rect / 2), HEIGHT / 2))
        SCREEN.blit(self.inst, ((WIDTH / 2) - (self.inst_rect / 2), HEIGHT - 50))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(500)
        self.update()
