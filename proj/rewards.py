import pygame
from proj.flyingObject import FlyingObject
import random


class RewardOne(FlyingObject):

    def __init__(self):
        super().__init__()
        r = random.randint(0, 1)
        if r:
            self.direction = -1
        else:
            self.direction = 1
        self.value = 15

        self.x_speed = 10
        self.y_speed = 4
        self.normal_count = 0
        self.normal_images = []

        self.load_resources()

    def load_resources(self):
        for i in range(1, 9):
            image = pygame.image.load("../images/xx"+str(i)+".png")
            self.normal_images.append(image)
        self.current_image = self.normal_images[0]

    def get_width(self):
        return self.normal_images[0].get_width()

    def get_height(self):
        return self.normal_images[0].get_height()

    def update_image(self, normal_rate=2):
        self.normal_count += 1
        index = self.normal_count // normal_rate
        if index < len(self.normal_images):
            self.current_image = self.normal_images[index]
        else:
            self.normal_count = 0

    def update_position(self):

        if self.x <= 0 or self.x > 510 - self.get_width():
            self.direction = - self.direction

        self.x += (self.direction * self.x_speed)
        self.y += self.y_speed


class RewardTwo(RewardOne):

    def __init__(self):
        super().__init__()
        self.value = 7

    def load_resources(self):
        img = pygame.image.load("../images/life.png")
        self.normal_images.append(img)
        self.current_image = img
