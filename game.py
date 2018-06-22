import pygame
from pygame.locals import *
from config import COLORS, SCREEN, WIDTH, ENEMY_POS
from player import Player
from enemy import Enemy
from item import Item

class Game:
    def __init__(self):
        """
        Creating the specific in game state
        """
        # Game player
        self.player = Player()

        # Enemy
        self.enemy = Enemy()

        # Item
        self.item = Item()

        # Create a font
        self.font = pygame.font.Font(None, 24)

        # Launching
        self.run = True
        self.draw()

    def scoring(self):
        """
        Scoring system
        :return: score
        """
        get_score_value = str(self.player.check_score())
        return get_score_value

    def remake_item(self):
        self.item = Item()

    def update(self):
        """
        Event loop
        """
        while self.run:
            for event in pygame.event.get():

                #Pressing a key
                if event.type == KEYDOWN:

                    # up
                    if event.key == K_UP:
                        self.player.moveup()

                    # downn
                    if event.key == K_DOWN:
                        self.player.movedown()

                    # right
                    if event.key == K_RIGHT:
                        self.player.moveright()

                    # left
                    if event.key == K_LEFT:
                        self.player.moveleft()

                # If quit or at the enemy position : Exit
                elif event.type == QUIT or self.player.rect.x == 200 and self.player.rect.y == 200:
                    if int(self.player.score) > 1:
                        file = open('score.txt', 'w')
                        file.write(f"You got {self.player.score} points !")
                        file.close()
                    self.run = False

            if self.player.rect.colliderect(self.item.rect):
                self.player.scoring_up()
                self.remake_item()

            pygame.time.wait(200)
            self.draw()

    def draw(self):
        """
        Fill background and blit everything to the screen
        """
        score_value = self.scoring()
        score = self.font.render(score_value, 1, (COLORS["WHITE"]))
        score_rect = (self.font.size(score_value))[0]

        # Fill background
        SCREEN.fill(COLORS["BLACK"])

        # Blit everything to the screen
        SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))
        SCREEN.blit(self.enemy.image, (ENEMY_POS))
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        SCREEN.blit(score, ((WIDTH - score_rect) - 20, 20))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(200)
        self.update()
