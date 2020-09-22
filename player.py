from pygame.sprite import Sprite
import pygame

GROUND = 750
V = 8
SPEED = 50
LIVES = 5


class Player(Sprite):
    def __init__(self, screen_width, screen_height, x=20, y=GROUND, speed=SPEED, v=V, m=3):
        Sprite.__init__(self)
        self.direction = 'R' #right
        self.image = pygame.image.load('./resources/images/player.png')
        self.image = pygame.transform.scale(self.image, (245, 245))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed
        self.v = v
        self.m = m
        self.is_jump = False
        self.lives = LIVES

        self.screen_width = screen_width
        self.screen_height = screen_height

    def jump(self):
        self.is_jump = True

    def update(self):
        self.speed = 0

        info = pygame.key.get_pressed()

        if info[pygame.K_LEFT]:
            if self.rect.x > 0:
                if self.direction == 'R':
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.direction = 'L'
                self.speed = -SPEED
        if info[pygame.K_RIGHT]:
            if self.rect.right < self.screen_width:
                if self.direction == 'L':
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.direction = 'R'
                self.speed = SPEED

        self.rect.x += self.speed


        if self.is_jump:
            if self.v > 0:
                f = 0.5 * self.m * self.v * self.v   # (m * v^2) / 2
            else:
                f = -0.5 * self.m * self.v * self.v
            self.rect.y -= f
            self.v -= 1

            if self.rect.y >= GROUND:
                self.rect.y = GROUND
                self.is_jump = False
                self.v = V

