import pygame
import os
from pygame.locals import *

from config import ASSETS_DIR, COLORS, SCREEN, SCREEN_W, SCREEN_H


class End:
    def __init__(self):

        # Text fonts
        font = pygame.font.Font(None, 48)
        inst_font = pygame.font.Font(None, 24)

        # Texts
        text_content = "The end"
        inst_content = "(Close to quit)"

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
        self.status = 0
        self.draw()

    def update(self):
        """
        Event loop with quit abilities
        """
        while self.run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.status = 0
                    self.run = False
                    return self.status

                elif event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[K_r]:
                        self.status = 1
                        self.run = False
                        return self.status


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
        SCREEN.blit(self.score, ((SCREEN_W / 2) - (self.score_rect / 2), SCREEN_H - 20))

        # Blit everything to the screen
        SCREEN.blit(self.text, ((SCREEN_W / 2) - (self.text_rect / 2), SCREEN_H / 2))
        SCREEN.blit(self.inst, ((SCREEN_W / 2) - (self.inst_rect / 2), SCREEN_H - 50))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(500)
        self.update()
