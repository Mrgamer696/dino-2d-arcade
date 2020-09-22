import pygame
import math
from time import sleep
from pygame.sprite import Sprite, Group
from  pygame.sprite import spritecollide
from player import Player
from item import FruitItem, BonusItem
from constants import *
from random import randint


class App:
    def __init__(self, window_width=800, window_height=600, direction='R'):
        self.all_sprites = Group()
        self.items = Group()
        self.bonuses = Group()

        self.window_width = window_width
        self.window_height = window_height
        self.direction = direction
        self.items_count = 6
        self.running = True
        self.display_surf = None
        self.image_surf = None
        self.scores = 0
        self.red_heart, self.black_heart = self.load_hearts()
        self.clock = pygame.time.Clock()
        self.lost = False

    def load_hearts(self):
        red_heart = pygame.image.load('resources/images/live_active.png')
        red_heart = pygame.transform.scale(red_heart, (128, 128))
        black_heart = pygame.image.load('resources/images/live_unactive.png')
        black_heart = pygame.transform.scale(black_heart, (128, 128))
        gold_heart = pygame.image.load('resources/images/live_bonus.png')
        gold_heart = pygame.transform.scale(gold_heart, (128, 128))
        return red_heart, black_heart


    def on_init(self):
        pygame.init()
        pygame.mixer.init()

        info = pygame.display.Info()

        self.window_height = info.current_h
        self.window_width = info.current_w

        self.player = Player(self.window_width, self.window_height)
        self.total_lives = self.player.lives


        self.display_surf = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
        self.back = pygame.image.load('resources/images/back.jpg').convert()
        self.back = pygame.transform.scale(self.back, (info.current_w, info.current_h))


        self.all_sprites.add(self.player)

        for i in range(self.items_count):
            item = FruitItem(self.window_width, self.window_height)
            self.all_sprites.add(item)
            self.items.add(item)

        self.jump_sound = pygame.mixer.Sound('resources/sounds/jump2.wav')

        pygame.mixer.music.load('resources/sounds/intro.mp3')
        pygame.mixer.music.play(-1)

        self.font = pygame.font.SysFont('Arial Black', 120)
        self.scores_font = pygame.font.SysFont('Segoe UI Black', 85)

    def on_render(self):

        self.display_surf.blit(self.back, [0, 0])
        k = 35
        for i in range(self.player.lives):
            self.display_surf.blit(self.red_heart, [k, 80])
            k += 145

        for i in range(self.total_lives - self.player.lives):
            self.display_surf.blit(self.black_heart, [k, 80])
            k += 145

        if self.player.lives > 0:
            self.all_sprites.update()

        self.all_sprites.draw(self.display_surf)

        if self.lost:
            text_lost_surface = self.font.render('GAME OVER!', False, RED_COLOR)
            self.display_surf.blit(text_lost_surface, (self.window_width // 2 - text_lost_surface.get_width() // 2, self.window_height // 2 - 30))

        text_scores_surface = self.scores_font.render('Scores: ' + str(self.scores), False, WHITE_COLOR)
        self.display_surf.blit(text_scores_surface, (self.window_width - text_scores_surface.get_width() - 30, 45))

        pygame.display.flip()
        sleep(0.06)

    def on_execute(self):
        self.on_init()
        while self.running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                if not self.player.is_jump:
                    pygame.mixer.Sound.play(self.jump_sound)
                self.player.jump()
            elif keys[pygame.K_ESCAPE]:
                self.running = False

            guess = randint(1, 400)
            if guess == 7:
                bonus = BonusItem(self.window_width, self.window_height)
                self.bonuses.add(bonus)
                self.all_sprites.add(bonus)


            collided = spritecollide(self.player, self.items, False)
            self.scores += len(collided)
            for item in collided:
                item.teleport()

            collided = spritecollide(self.player, self.bonuses, True) #[c1]
            if collided:
                if self.player.lives < self.total_lives:
                    self.player.lives += 1

            for item in self.items:
                if item.rect.y > self.window_height:
                    item.teleport()
                    self.player.lives -= 1

            for bonus in self.bonuses:
                if bonus.rect.y > self.window_height:
                    bonus.kill()

            self.on_render()

            if self.player.lives == 0 and not self.lost:
                self.on_render()
                self.lost = True

            self.clock.tick(100)
        pygame.quit()


game = App()
game.on_execute()









