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
        self.items_in_level = 3

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

        # Ether item
        self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)), "ether")
        self.items.append(self.item)

        # Needle item
        self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)), "needle")
        self.items.append(self.item)

        # Pipe
        self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)), "pipe")
        self.items.append(self.item)

        # Collecting image feedback status
        self.draw_item = False

        # XL image when player catch sprite
        self.ether_xl_image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/ether_xl.png"))
        self.needle_xl_image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/needle_xl.png"))
        self.pipe_xl_image = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/pipe_xl.png"))

        # XL rect for centering display
        self.ether_xl_rect = self.ether_xl_image.get_rect()
        self.needle_xl_rect = self.needle_xl_image.get_rect()
        self.pipe_xl_rect = self.pipe_xl_image.get_rect()

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

    def remake_item(self, kind):
        """
        Remake an item when collide to a wall, enemy or player rect
        """
        # Remove item
        self.items.remove(self.item)
        self.items_in_level -= 1

        # Remake item
        self.item = Item((randint(64, SCREEN_W - 64), randint(64, SCREEN_H - 64)), kind)
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
                    self.remake_item(self.item.kind)

            # Test item generation with enemy
            if self.item.rect.colliderect(self.enemy.rect):
                self.remake_item(self.item.kind)

            # Test item generation with player
            if self.item.rect.colliderect(self.player.rect):
                self.remake_item(self.item.kind)

    def check_items_collecting(self):
        """
        Actions when player is collecting items
        """
        self.draw_item = False
        for self.item in self.items:

            keys = pygame.key.get_pressed()

            # Checking user event ( player is moving )
            if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:

                # Player and Items are colliding
                if self.player.rect.colliderect(self.item.rect):

                    # Needle collecting feedback
                    if self.item.kind == "needle":
                        self.draw_item = "needle"

                    # Ether collecting feedback
                    elif self.item.kind == "ether":
                        self.draw_item = "ether"

                    # Pipe collecting feedback
                    elif self.item.kind == "pipe":
                        self.draw_item = "pipe"

                    # Countdown items
                    self.items_in_level -= 1

                    # Collecting sound feedback
                    self.sound_point.play()

                    # Scoring up
                    self.player.scoring_up()

                    # Remove the item
                    self.items.remove(self.item)

    def handling_music(self, keys):
        """
        Handle the music
        :param keys: Pressed keys
        """

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

    def walking_in_maze(self, keys):
        """
        Player is evolving in the maze
        :param keys: Pressed keys
        """

        # Check if the game is paused
        if not self.pause:

            # up
            if keys[K_UP]:

                # Check the player position before moves
                if self.player.rect.y > 0:
                    self.player.move_up()

                    # Prevent player colliding walls
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):

                            # Going back
                            self.player.move_down()

            # down
            elif keys[K_DOWN]:

                # Check the player position before moves
                if self.player.rect.y + self.player.speed < SCREEN_H:
                    self.player.move_down()

                    # Prevent player colliding walls
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):

                            # Going back
                            self.player.move_up()

            # right
            elif keys[K_RIGHT]:
                # Check the player position before moves
                if self.player.rect.x + self.player.speed < SCREEN_W:
                    self.player.move_right()

                    # Prevent player colliding walls
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):

                            # Going back
                            self.player.move_left()

            # left
            elif keys[K_LEFT]:
                # Check the player position before moves
                if self.player.rect.x > 0:
                    self.player.move_left()

                    # Prevent player colliding walls
                    for self.wall in self.walls:
                        if self.player.rect.colliderect(self.wall.rect):

                            # Going back
                            self.player.move_right()

    def checking_player_colliding_enemy(self):
        """
        Check if player is colliding with enemy
        :return: (bool)
        """
        if self.player.rect.colliderect(self.enemy.rect):
            self.player.collides_enemy = True
            return True

    def scoring(self):
        """
        Scoring system
        :return: score
        """
        get_score_value = str(self.player.score)
        return get_score_value

    def check_for_ending(self, event):
        """
        Check if the game will be terminated
        :param: event: Captured events
        """
        if self.player.collides_enemy:

            if self.items_in_level == 0:
                self.win_or_fail("win")
            else:
                self.win_or_fail("fail")

        if event.type == QUIT:
            self.win_or_fail("close")

    def win_or_fail(self, ending):
        """
        Those actions differs when game is terminated
        :param : ending : The ending status of the game
        :return : status ( always 0 if only one level )
        """
        ending_status = False
        if ending == "win":
            self.sound_win.play()
            ending_status = "Victory ! You made the guard falling asleep !"

        elif ending == "close":
            self.sound_fail.play()
            ending_status = "You close before facing your enemy! Game Over..."

        elif ending == "fail":
            self.sound_fail.play()
            ending_status = "GAME OVER !!"

        # Fading out music
        self.music.fadeout()

        # Writing score in text file
        file = open('score.txt', 'w')
        file.write(ending_status)
        file.close()

        # Exit game loop
        self.run = False

        # Return status
        # ( in order to pass to the next in the future)
        return self.status

    def update(self):
        """
        Event loop
        """

        # Game loop is running
        while self.run:

            # Capture user events
            for event in pygame.event.get():
                self.check_for_ending(event)

                # Pressing a key
                keys = pygame.key.get_pressed()
                self.handling_music(keys)
                self.walking_in_maze(keys)
                self.checking_player_colliding_enemy()

            # Check if player is collecting items
            self.check_items_collecting()

            # Prevent too many recursion errors
            pygame.time.wait(50)

            # Draw the updated game
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

        # Draw walls
        for self.wall in self.walls:
            SCREEN.blit(self.wall.image, (self.wall.rect.x, self.wall.rect.y))

        # Draw items
        for self.item in self.items:
            if self.item.rect:
                SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))

        # Draw music sign
        if self.music.is_playing:
            SCREEN.blit(self.music.play_img, (SCREEN_W - 35, SCREEN_H - 35))
        else:
            SCREEN.blit(self.music.stop_img, (SCREEN_W - 35, SCREEN_H - 35))

        # Draw enemy
        SCREEN.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))

        # Draw player
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Draw score
        SCREEN.blit(score, ((SCREEN_W - score_rect) - 20, 20))

        # Draw text pause
        if self.pause:
            SCREEN.blit(self.text, ((SCREEN_W / 2) - (self.text_rect / 2), SCREEN_H / 2))

        # Draw items colling feedback
        if self.draw_item == "needle":
            SCREEN.blit(self.needle_xl_image, (
                (SCREEN_W // 2 - self.needle_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.needle_xl_rect.y * 2) / 2))
        elif self.draw_item == "ether":
            SCREEN.blit(self.ether_xl_image, (
                (SCREEN_W // 2 - self.ether_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.ether_xl_rect.y * 2) / 2))
        elif self.draw_item == "pipe":
            SCREEN.blit(self.pipe_xl_image, (
                (SCREEN_W // 2 - self.pipe_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.pipe_xl_rect.y * 2) / 2))

        # Update the game
        pygame.display.flip()

        # Prevent too many recursion errors
        pygame.time.wait(50)

        # Check for updates
        self.update()
