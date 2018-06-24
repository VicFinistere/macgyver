import pygame
from pygame.locals import *
from config import COLORS, SCREEN, WIDTH
from player import Player
from enemy import Enemy
from item import Item
from wall import Wall


class Game:
    def __init__(self):
        """
        Creating the specific in game state
        """
        # Level
        self.level_file = "level.txt";
        with open(self.level_file, "r") as level:
            self.walls = []
            self.items = []
            self.collide_ennemy = False
            x = y = 0

            for row in level:
                for col in row:
                    if col == "P":
                        self.player = Player((x, y))
                    elif col == "E":
                        self.enemy = Enemy((x, y))
                    elif col == "W":
                        self.wall = Wall((x, y))
                        self.walls.append(self.wall)
                    elif col == "I":
                        self.item = Item((x, y))
                        self.items.append(self.item)
                    x += 30
                x = 0
                y += 30

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

    def update(self):
        """
        Event loop
        """

        while self.run:
            for event in pygame.event.get():

                if event.type == QUIT or self.collide_ennemy:
                    if int(self.player.score) > 1:
                        file = open('score.txt', 'w')
                        file.write(f"You got {self.player.score} points !")
                        file.close()
                    self.run = False

                # Pressing a key
                if event.type == KEYDOWN:

                    # up
                    if event.key == K_UP:
                        self.player.moveup()
                        for self.wall in self.walls:
                            if self.player.rect.colliderect(self.wall.rect):
                                self.player.movedown()
                    # down
                    if event.key == K_DOWN:
                        self.player.movedown()
                        for self.wall in self.walls:
                            if self.player.rect.colliderect(self.wall.rect):
                                self.player.moveup()
                    # right
                    if event.key == K_RIGHT:
                        self.player.moveright()
                        for self.wall in self.walls:
                            if self.player.rect.colliderect(self.wall.rect):
                                self.player.moveleft()
                    # left
                    if event.key == K_LEFT:
                        self.player.moveleft()
                        for self.wall in self.walls:
                            if self.player.rect.colliderect(self.wall.rect):
                                self.player.moveright()

                    if self.player.rect.colliderect(self.enemy.rect):
                        self.collide_ennemy = True

            for self.item in self.items:
                if self.item.rect:
                    if self.player.rect.colliderect(self.item.rect):
                        self.player.scoring_up()
                        self.items.remove(self.item)

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
        SCREEN.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        SCREEN.blit(score, ((WIDTH - score_rect) - 20, 20))
        for self.wall in self.walls:
            SCREEN.blit(self.wall.image, (self.wall.rect.x, self.wall.rect.y))

        for self.item in self.items:
            if self.item.rect:
                SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(200)
        self.update()
