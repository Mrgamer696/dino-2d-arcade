import pygame
from pygame.sprite import Sprite
from random import choice, randint
import random


class Item(Sprite):
    def __init__(self, screen_width, screen_height, dificulty):
        Sprite.__init__(self)
        self.item_width = 128
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.dificulty = dificulty

    def teleport(self):
        self.rect.x = randint(0, self.screen_width - self.item_width)
        self.rect.y = randint(-200, -100)
        if self.dificulty == "EASY":
            self.speed = randint(2, 12)
        elif self.dificulty == "MEDIUM":
            self.speed = randint(8, 16)
        elif self.dificulty == "HARD":
            self.speed = randint(12, 22)

    def update(self):
        self.rect.y += self.speed


class FruitItem(Item):
    def __init__(self, screen_width, screen_height, difictulty):
        Item.__init__(self, screen_width, screen_height, difictulty)
        self.filenames = ['apple1.png', 'Banana.png']
        self.image = pygame.image.load('resources/images/' + choice(self.filenames))
        self.image = pygame.transform.scale(self.image, (self.item_width, self.item_width))
        self.rect = self.image.get_rect()
        self.teleport()

    def teleport(self):
        self.image = pygame.image.load('resources/images/' + choice(self.filenames))
        self.image = pygame.transform.scale(self.image, (self.item_width, self.item_width))
        super().teleport()


class BonusItem(Item):
    def __init__(self, screen_width, screen_height, dificulty):
        Item.__init__(self, screen_width, screen_height, dificulty)
        filenames = ['bonus.png', 'bonus2.png']
        self.image = pygame.image.load('resources/images/' + choice(filenames))
        self.rect = self.image.get_rect()
        self.teleport()