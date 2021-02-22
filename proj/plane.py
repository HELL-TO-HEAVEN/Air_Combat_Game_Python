import pygame
from proj.flyingObject import FlyingObject


class Plane(FlyingObject):
    def __init__(self):

        super().__init__()

        # 飞机属性
        self.hp = 5
        self.be_hit = False
        # 飞机资源容器
        self.normal_images = []
        self.hit_images = []
        self.destroy_images = []
        self.destroy_music = None
        # 计时器
        self.destroy_count = 0
        self.hit_count = 0
        self.normal_count = 0

    def update_image(self, normal_rate=2, hit_rate=4, destroy_rate=4):
        # 如果死亡
        if self.hp <= 0:
            self.destroy_count += 1

            if self.destroy_count == 1:
                # 播放死亡音乐
                self.destroy_music.play()

            index = self.destroy_count // destroy_rate

            # 如果播放完
            if index < len(self.destroy_images):
                self.current_image = self.destroy_images[index]
            else:
                self.can_clear = True

        # 如果活着 被击中
        elif self.be_hit:
            self.hit_count += 1

            index = self.hit_count // hit_rate

            if index < len(self.hit_images):
                self.current_image = self.hit_images[index]
            else:
                self.be_hit = False
                self.hit_count = 0
        # 正常
        else:
            self.normal_count += 1
            index = self.normal_count // normal_rate
            if index == len(self.normal_images):
                self.normal_count = 0
                index = 0
            self.current_image = self.normal_images[index]
