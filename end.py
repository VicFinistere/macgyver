import pygame
from pygame.locals import *

from config import COLORS, SCREEN, WIDTH, HEIGHT

class End:
    def __init__(self):
        # Create a font
        self.font = pygame.font.Font(None, 24)

        # Texts
        self.text_content = "The end"
        self.inst_content = "(Click again to quit)"

        # Pygame Texts Elements
        self.inst = self.font.render(self.inst_content, 1, (COLORS["WHITE"]))
        self.inst_rect = (self.font.size(self.inst_content))[0]
        self.text = self.font.render(self.text_content, 1, (COLORS["WHITE"]))
        self.text_rect = (self.font.size(self.text_content))[0]

        # Get the score from file
        self.score_file = open("score.txt", "r")
        self.score_content = self.score_file.read()
        self.score_file.close()

        # Victory Message
        self.score = self.font.render(self.score_content, 1, (COLORS["WHITE"]))
        self.score_rect = (self.font.size(self.score_content))[0]

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
        SCREEN.fill(COLORS["BLACK"])

        # VICTORY CASE
        SCREEN.blit(self.score, ((WIDTH / 2) - (self.score_rect / 2), HEIGHT - 20))

        # Blit everything to the screen
        SCREEN.blit(self.text, ((WIDTH / 2) - (self.text_rect / 2), HEIGHT / 2))
        SCREEN.blit(self.inst, ((WIDTH / 2) - (self.inst_rect / 2), HEIGHT - 50))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(500)
        self.update()
