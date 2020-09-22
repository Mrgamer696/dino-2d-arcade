import pygame
from pygame.sprite import Sprite
from random import choice, randint
import random


class Item(Sprite):
    def __init__(self, screen_width, screen_height):
        Sprite.__init__(self)
        self.item_width = 128
        self.screen_width = screen_width
        self.screen_height = screen_height

    def teleport(self):
        self.rect.x = randint(0, self.screen_width - self.item_width)
        self.rect.y = randint(-200, -100)
        self.speed = randint(7, 15)

    def update(self):
        self.rect.y += self.speed


class FruitItem(Item):
    def __init__(self, screen_width, screen_height):
        Item.__init__(self, screen_width, screen_height)
        self.filenames = ['apple.png', 'Banana.png']
        self.image = pygame.image.load('resources/images/' + choice(self.filenames))
        self.image = pygame.transform.scale(self.image, (self.item_width, self.item_width))
        self.rect = self.image.get_rect()
        self.teleport()

    def teleport(self):
        self.image = pygame.image.load('resources/images/' + choice(self.filenames))
        self.image = pygame.transform.scale(self.image, (self.item_width, self.item_width))
        super().teleport()


class BonusItem(Item):
    def __init__(self, screen_width, screen_height):
        Item.__init__(self, screen_width, screen_height)
        filenames = ['bonus.png', 'bonus2.png']
        self.image = pygame.image.load('resources/images/' + choice(filenames))
        self.rect = self.image.get_rect()
        self.teleport()