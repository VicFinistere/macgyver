"""
This class makes the level
"""
import os
import pytmx
import pygame
from player import Player
from enemy import Enemy
from wall import Wall
from item import Item
from config import ASSETS_DIR, SCREEN_W, SCREEN_H
from random import randint


class Level:
    """
    Class Level
    """

    def __init__(self):
        self.background = pygame.image.load(os.path.join(ASSETS_DIR, "gfx/background.png"))
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

        # Item test position
        self.test_item()
