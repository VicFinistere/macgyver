import pygame
import os
from pygame.locals import *
import pytmx
from config import COLORS, SCREEN, WIDTH
from player import Player
from enemy import Enemy
from item import Item
from wall import Wall
from config import ASSETS_DIR

class Game:
    def __init__(self):
        """
        Creating the specific in game state
        """
        # Level
        level_file = os.path.join(ASSETS_DIR, "gfx/level.tmx")
        level = pytmx.load_pygame(level_file)
        self.walls = []
        self.items = []
        wall_tiles = 0
        item_tiles = 1
        enemy_tiles = 2
        player_tiles = 3

        self.collide_enemy = False

        for row in range(15):
            for col in range(15):
                # Walls in tmx file
                wall = level.get_tile_image(row, col, wall_tiles)
                if wall is not None:
                    self.wall = Wall((row, col))
                    self.walls.append(self.wall)

                # Item in tmx file
                item = level.get_tile_image(row, col, item_tiles)
                if item is not None:
                    self.item = Item((row, col))
                    self.items.append(self.item)

                # Enemy in tmx file
                enemy = level.get_tile_image(row, col, enemy_tiles)
                if enemy is not None:
                    self.enemy = Enemy((row, col))

                # Player in tmx file
                player = level.get_tile_image(row, col, player_tiles)
                if player is not None:
                    self.player = Player((row, col))

        # Create a font
        self.font = pygame.font.Font(None, 24)

        # Sounds
        self.sound_point = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/point.flac"))
        self.sound_win = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/win.ogg"))
        self.sound_fail = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/fail.wav"))
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

                if event.type == QUIT or self.collide_enemy:
                    if int(self.player.score) > 1:
                        self.sound_win.play()
                        file = open('score.txt', 'w')
                        file.write(f"You got {self.player.score} points !")
                        file.close()
                    else:
                        self.sound_fail.play()
                    self.run = False

                # Pressing a key

                keys = pygame.key.get_pressed()
                # up
                if keys[K_UP]:
                    self.player.moveup()
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):
                            self.player.movedown()

                # down
                elif keys[K_DOWN]:
                    self.player.movedown()
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):
                            self.player.moveup()


                # right
                elif keys[K_RIGHT]:
                    self.player.moveright()
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):
                            self.player.moveleft()


                # left
                elif keys[K_LEFT]:
                    self.player.moveleft()
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):
                            self.player.moveright()


                if self.player.rect.colliderect(self.enemy.rect):
                    self.collide_enemy = True

            for self.item in self.items:
                if self.item.rect:
                    if self.player.rect.colliderect(self.item.rect):
                        self.sound_point.play()
                        self.player.scoring_up()
                        self.items.remove(self.item)

            pygame.time.wait(50)
            self.draw()

    def draw(self):
        """
        Fill background and blit everything to the screen
        """
        score_value = self.scoring()
        score = self.font.render(score_value, 1, (COLORS["WHITE"]))
        score_rect = (self.font.size(score_value))[0]

        # Fill background
        background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/background.png"))
        SCREEN.blit(background, (0, 0))

        # Blit everything to the screen
        for self.wall in self.walls:
            SCREEN.blit(self.wall.image, (self.wall.rect.x, self.wall.rect.y))

        for self.item in self.items:
            if self.item.rect:
                SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))
        SCREEN.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        SCREEN.blit(score, ((WIDTH - score_rect) - 20, 20))
        pygame.display.flip()
        pygame.display.flip()
        self.update()
