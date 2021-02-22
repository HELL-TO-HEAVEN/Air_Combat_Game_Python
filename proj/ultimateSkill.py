import pygame
from proj.flyingObject import FlyingObject
from pygame import Rect


'''大招'''


class UltimateSkill(FlyingObject):

    def __init__(self, hero, width, height, interval):
        super().__init__()
        self.hero = hero
        self.hurt = 1
        self.width = width
        self.height = height
        self.image_rect = Rect(0, 0, width, height)
        self.interval = interval
        self.normal_count = 0
        # -5是微调
        self.x = self.hero.x + self.hero.get_width() / 2 - self.get_width() / 2 - 4
        # 加10是微调
        self.y = self.hero.y - self.get_height() + 10

        self.load_resources()

    def load_resources(self):
        self.current_image = pygame.image.load("../images/dazhao.png")

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def blit_me(self, screen):
        screen.blit(self.current_image, (self.x, self.y), self.image_rect)

    def update_image_rect(self, normal_rate = 2):
        self.normal_count += 1
        index = self.normal_count // normal_rate
        if index == 8:
            index = 0
            self.normal_count = 0
        self.image_rect.left = index * self.interval

    def update_position(self):
        self.x = self.hero.x + self.hero.get_width()/2 - self.get_width()/2 - 4
        # 加10是微调
        self.y = self.hero.y - self.get_height() + 10

    def get_rect(self):
        # 微调
        rect = Rect(self.x + 10, 0, self.get_width() - 20, self.hero.y)
        return rect
