from proj.flyingObject import FlyingObject
import pygame


class Shield(FlyingObject):

    def __init__(self, hero):
        super().__init__()

        self.hero = hero
        self.normal_images = []
        self.normal_count = 0
        self.load_resource()
        self.x = self.hero.x + self.hero.get_width() / 2 - self.get_width() / 2
        # -10是微调
        self.y = self.hero.y + self.hero.get_height() / 2 - self.get_height() / 2 - 20

    def load_resource(self):
        for i in range(1, 7):
            img = pygame.image.load("../images/hudun"+str(i)+".png")
            self.normal_images.append(img)
        self.current_image = self.normal_images[0]

    def update_image(self, normal_rate=2):
        self.normal_count += 1
        index = self.normal_count // normal_rate
        if index < len(self.normal_images):
            self.current_image = self.normal_images[index]
        else:
            self.normal_count = 0

    def update_position(self):
        self.x = self.hero.x + self.hero.get_width()/2 - self.get_width()/2
        self.y = self.hero.y + self.hero.get_height()/2 - self.get_height()/2 - 20
