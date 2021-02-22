from proj.plane import Plane
from proj.bullets import *


class Hero(Plane):
    """英雄机"""
    def __init__(self):
        super().__init__()
        self.max_hp = 60
        self.max_mp = 400
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.load_resource()

    def load_resource(self):
        for i in range(2, 4):
            image = pygame.image.load("../images/hero2"+str(i)+".png")
            self.normal_images.append(image)
        self.current_image = self.normal_images[0]

    def update_image(self, normal_rate=2, hit_rate=2, destroy_rate=2):
        self.normal_count += 1
        index = self.normal_count // normal_rate
        if index == len(self.normal_images):
            self.normal_count = 0
            index = 0
        self.current_image = self.normal_images[index]

        if self.be_hit:
            self.hit_count += 1
            if self.hit_count == 50:
                self.hit_count = 0
                self.be_hit = False
