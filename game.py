"""
Game Scene : This is where all the game logic is made
"""
import os
import pygame
from pygame.locals import *
from config import ASSETS_DIR, COLORS, SCREEN, SCREEN_W, SCREEN_H
from music import Music
from level import Level


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

        # Pause text
        pause_content = " (P)ause "

        # Pygame Texts Elements
        self.text = font.render(pause_content, 1, (COLORS["WHITE"]))
        self.text_rect = (font.size(pause_content))[0]

        # Create the level
        self.level = Level()

        # Player
        self.player = self.level.player

        # Enemy
        self.enemy = self.level.enemy

        # Walls
        self.walls = self.level.walls

        # Items
        self.items = self.level.items

        # Item
        self.item = self.level.item

        # Item counter
        self.items_in_level = self.level.items_in_level

        # Item test position
        self.level.test_item()

        # Collecting image feedback status
        self.draw_item = False

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

    def draw_level(self):
        """
        Draw level
        """
        # Draw walls
        for self.wall in self.walls:
            SCREEN.blit(self.wall.image, (self.wall.rect.x, self.wall.rect.y))

        # Draw items
        for self.item in self.items:
            if self.item.rect:
                SCREEN.blit(self.item.image, (self.item.rect.x, self.item.rect.y))

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

    def handle_music(self, keys):
        """
        Handle the pause and the music
        :param keys: Pressed keys
        """

        # Music keys
        if keys[K_p] or keys[K_s]:

            # Pause the music ( playing by default )
            if self.music.is_playing:
                self.music.is_playing = False
                self.music.pause()

            # Restart the music ( Stop the pause )
            elif not self.music.is_playing:
                self.music.is_playing = True
                self.music.unpause()

    def handle_pause(self, keys):
        """
        Handle the pause
        :param keys: Pressed keys
        """
        # Pause key
        if keys[K_p]:

            # Pause the game
            if self.pause:
                self.pause = False

            # Restart the game
            else:
                self.pause = True

    def draw_music_status(self):
        """
        Draw music status image
        """
        if self.music.is_playing:
            SCREEN.blit(self.music.play_img, (SCREEN_W - 35, SCREEN_H - 35))
        else:
            SCREEN.blit(self.music.stop_img, (SCREEN_W - 35, SCREEN_H - 35))

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

    def draw_score(self):
        # Draw score
        score_value = self.scoring()
        score = self.font.render(score_value, 1, (COLORS["WHITE"]))
        score_rect = (self.font.size(score_value))[0]
        SCREEN.blit(score, ((SCREEN_W - score_rect) - 20, 20))

    def draw_collided_item(self):
        """
        Draw collided items image
        """
        if self.draw_item == "needle":
            SCREEN.blit(self.item.needle_xl_image, (
                (SCREEN_W // 2 - self.item.needle_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.item.needle_xl_rect.y * 2) / 2))
        elif self.draw_item == "ether":
            SCREEN.blit(self.item.ether_xl_image, (
                (SCREEN_W // 2 - self.item.ether_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.item.ether_xl_rect.y * 2) / 2))
        elif self.draw_item == "pipe":
            SCREEN.blit(self.item.pipe_xl_image, (
                (SCREEN_W // 2 - self.item.pipe_xl_rect.x * 2) / 2,
                (SCREEN_H // 2 - self.item.pipe_xl_rect.y * 2) / 2))

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
                self.handle_pause(keys)
                self.handle_music(keys)
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

        # Fill background
        background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/background.png"))
        SCREEN.blit(background, (0, 0))

        # Draw level
        self.draw_level()

        # Draw music sign
        self.draw_music_status()

        # Draw enemy
        SCREEN.blit(self.enemy.image, (self.enemy.rect.x, self.enemy.rect.y))

        # Draw player
        SCREEN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))

        # Draw score
        self.draw_score()

        # Draw text pause
        if self.pause:
            SCREEN.blit(self.text, ((SCREEN_W / 2) - (self.text_rect / 2), SCREEN_H / 2))

        # Draw collided items feedback
        self.draw_collided_item()

        # Update the game
        pygame.display.flip()

        # Prevent too many recursion errors
        pygame.time.wait(50)

        # Check for updates
        self.update()
