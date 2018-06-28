"""
Game Scene : This is where all the game logic is made
"""
import os
import pygame
from pygame.locals import *
import pytmx
from config import COLORS, SCREEN, SCREEN_W, SCREEN_H
from music import Music
from player import Player
from enemy import Enemy
from item import Item
from wall import Wall
from config import ASSETS_DIR
from random import randint


class Game:
    def __init__(self):
        """
        Game Scene
        """
        # Music
        self.music = Music()
        self.music.play()

        # Pause
        self.pause = False

        # Font
        font = pygame.font.Font(None, 24)

        # Texts
        pause_content = " (P)ause "

        # Pygame Texts Elements
        self.text = font.render(pause_content, 1, (COLORS["WHITE"]))
        self.text_rect = (font.size(pause_content))[0]

        # Level
        level_file = os.path.join(ASSETS_DIR, "gfx", "level.tmx")
        level = pytmx.load_pygame(level_file)
        self.walls = []
        self.items = []
        wall_tiles = 0
        enemy_tiles = 2
        player_tiles = 3

        # We just want 4 items by level
        self.items_in_level = 10

        self.collide_enemy = False

        for row in range(15):
            for col in range(15):
                # Walls in tmx file
                wall = level.get_tile_image(row, col, wall_tiles)
                if wall is not None:
                    self.wall = Wall((row, col))
                    self.walls.append(self.wall)

                # Enemy in tmx file
                enemy = level.get_tile_image(row, col, enemy_tiles)
                if enemy is not None:
                    self.enemy = Enemy((row, col))

                # Player in tmx file
                player = level.get_tile_image(row, col, player_tiles)
                if player is not None:
                    self.player = Player((row, col))

        for i in range(self.items_in_level):
            self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)))
            self.items.append(self.item)

        # Create a font
        self.font = pygame.font.Font(None, 24)

        # Sounds
        self.sound_point = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/point.flac"))
        self.sound_win = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/win.ogg"))
        self.sound_fail = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sfx/fail.wav"))
        self.sound_rect_x, self.sound_rect_y = SCREEN_W - 35, SCREEN_H - 35

        # Launching
        self.run = True
        self.status = 0
        self.draw()

    def remake_item(self):
        """
        Remake an item when collide to a wall, enemy or player rect
        """
        self.items.remove(self.item)
        self.items_in_level -= 1
        self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)))
        self.items.append(self.item)
        self.items_in_level += 1

    def test_item(self):
        """
        Test of the random generation ( goal :  be able to catch it )
        """
        # Test items generation with walls
        for self.item in self.items:
            for self.wall in self.walls:
                if self.item.rect.colliderect(self.wall.rect):
                    self.remake_item()

            # Test item generation with enemy
            if self.item.rect.colliderect(self.enemy.rect):
                self.remake_item()

            # Test item generation with player
            if self.item.rect.colliderect(self.player.rect):
                self.remake_item()

    def scoring(self):
        """
        Scoring system
        :return: score
        """
        get_score_value = str(self.player.score)
        return get_score_value

    def update(self):
        """
        Event loop
        """

        while self.run:

            for event in pygame.event.get():

                if self.collide_enemy:

                    if self.items_in_level == 0:
                        self.sound_win.play()
                        file = open('score.txt', 'w')
                        file.write(f"Victory ! You got all {self.player.score} Swiss Army Knife !")
                        file.close()
                        self.status = 0
                        self.run = False
                        return self.status

                    else:
                        self.sound_fail.play()
                        file = open('score.txt', 'w')
                        file.write("GAME OVER !!")
                        file.close()
                        self.music.fadeout()
                        self.status = 0
                        self.run = False
                        return self.status

                if event.type == QUIT:
                    self.sound_fail.play()
                    file = open('score.txt', 'w')
                    file.write("You close before facing your enemy! Game Over...")
                    file.close()
                    self.music.fadeout()
                    self.status = 0
                    self.run = False
                    return self.status
                    # Pressing a key

                keys = pygame.key.get_pressed()

                # Music keys
                if keys[K_p] or keys[K_s]:

                    # Pause the music ( playing by default )
                    if self.music.is_playing:
                        self.music.is_playing = False
                        self.music.pause()

                        # Pause text : on
                        if keys[K_p]:
                            self.pause = True

                    # Restart the music ( Stop the pause )
                    elif not self.music.is_playing:
                        self.music.is_playing = True
                        self.music.unpause()

                        # Pause text : off
                        if keys[K_p]:
                            self.pause = False

                # up
                if not self.pause:
                    if keys[K_UP]:
                        if self.player.rect.y > 0:
                            self.player.move_up()
                            for self.wall in self.walls:
                                if self.player.rect.colliderect(self.wall.rect):
                                    self.player.move_down()

                    # down
                    elif keys[K_DOWN]:
                        if self.player.rect.y + self.player.speed * 2 < SCREEN_H:
                            self.player.move_down()
                            for self.wall in self.walls:
                                if self.player.rect.colliderect(self.wall.rect):
                                    self.player.move_up()


                    # right
                    elif keys[K_RIGHT]:
                        if self.player.rect.x + self.player.speed * 2 < SCREEN_W:
                            self.player.move_right()
                            for self.wall in self.walls:
                                if self.player.rect.colliderect(self.wall.rect):
                                    self.player.move_left()


                    # left
                    elif keys[K_LEFT]:
                        if self.player.rect.x > 0:
                            self.player.move_left()
                            for self.wall in self.walls:
                                if self.player.rect.colliderect(self.wall.rect):
                                    self.player.move_right()

                # Collide with enemy
                if self.player.rect.colliderect(self.enemy.rect):
                    self.collide_enemy = True

            # Collect items
            for self.item in self.items:
                keys = pygame.key.get_pressed()
                if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
                    if self.player.rect.colliderect(self.item.rect):
                        self.items_in_level -= 1
                        self.sound_point.play()
                        self.player.scoring_up()
                        self.items.remove(self.item)

            pygame.time.wait(50)
            self.draw()

    def draw(self):
        """
        Fill background and blit everything to the screen
        """
        # Item test position
        self.test_item()

        score_value = self.scoring()
        score = self.font.render(score_value, 1, (COLORS["WHITE"]))
        score_rect = (self.font.size(score_value))[0]

        # Fill background
        background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/background.png"))
        SCREEN.blit(background, (0, 0))

        # Blit everything to the screen
        SCREEN.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        if self.pause:
            SCREEN.blit(self.text, ((SCREEN_W / 2) - (self.text_rect / 2), SCREEN_H / 2))

        for self.wall in self.walls:
            SCREEN.blit(self.wall.image, (self.wall.rect.x, self.wall.rect.y))

        for self.item in self.items:
            if self.item.rect:
                SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))
        SCREEN.blit(score, ((SCREEN_W - score_rect) - 20, 20))
        if self.music.is_playing:
            SCREEN.blit(self.music.play_img, (SCREEN_W - 35, SCREEN_H - 35))
        else:
            SCREEN.blit(self.music.stop_img, (SCREEN_W - 35, SCREEN_H - 35))
        pygame.display.flip()
        pygame.display.flip()
        pygame.time.wait(50)
        self.update()
