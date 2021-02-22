from proj.plane import Plane
import random
from proj.rewards import RewardOne, RewardTwo
import pygame


class EnemyOne(Plane):
    def __init__(self):
        super().__init__()
        self.y_speed = 10
        self.hurt = 2
        self.load_resources()

    def load_resources(self):
        # 音效
        self.destroy_music = pygame.mixer.Sound("../music/enemy1_down.wav")
        self.destroy_music.set_volume(0.2)

        # 加载死亡图片
        for i in range(1, 6):
            img = pygame.image.load("../images/enemy1" + str(i) + ".png")
            self.destroy_images.append(img)

        # 加载普通图片
        self.normal_images = self.destroy_images[0:1]

        # 加载击中图片
        self.hit_images = self.destroy_images[0:2]

        self.current_image = self.normal_images[0]

    "更新位置"
    def update_position(self):
        self.y += self.y_speed

    "按照传入概率掉落星星"
    def shoot_reward_star(self, probability):
        r = random.randint(0, 100)
        if r <= probability:
            xingxing = RewardOne()
            xingxing.x = self.x + self.get_width() / 2
            xingxing.y = self.y + self.get_height() / 2
            return xingxing
        else:
            return None

    "按照传入概率掉落生命值"
    def shoot_reward_life(self, probability):
        r = random.randint(0, 100)
        if r <= probability:
            life = RewardTwo()
            life.x = self.x + self.get_width() / 2
            life.y = self.y + self.get_height() / 2
            return life
        else:
            return None


class EnemyTwo(EnemyOne):

    def __init__(self):
        super().__init__()
        self.y_speed = 8
        self.hp = 20
        self.hurt = 4

    def load_resources(self):

        # 音效
        self.destroy_music = pygame.mixer.Sound("../music/enemy2_down.wav")
        self.destroy_music.set_volume(0.2)

        # 死亡
        for i in range(1, 6):
            img = pygame.image.load("../images/enemy2"+str(i)+".png")
            self.destroy_images.append(img)

        # 正常
        for i in range(1, 2):
            img = pygame.image.load("../images/enemy2"+str(i)+".png")
            self.normal_images.append(img)
        # 击打
        self.hit_images = self.destroy_images[0:3]
        self.hit_images.append(self.destroy_images[1])

        self.current_image = self.normal_images[0]


class EnemyThree(EnemyOne):
    def __init__(self):
        super().__init__()
        self.hurt = 6
        self.y_speed = 6
        self.hp = 40

    def load_resources(self):
        # 音效
        self.destroy_music = pygame.mixer.Sound("../music/enemy3_down.wav")
        self.destroy_music.set_volume(0.05)

        # 死亡图片
        for i in range(0, 8):
            img = pygame.image.load("../images/enemy3"+str(i)+".png")
            self.destroy_images.append(img)
        img1 = pygame.image.load("../images/enemy30.png")
        img2 = pygame.image.load("../images/enemy31.png")
        img3 = pygame.image.load("../images/enemy3_hit.png")
        img4 = pygame.image.load("../images/enemy32.png")
        img5 = pygame.image.load("../images/enemy33.png")
        img6 = pygame.image.load("../images/enemy33.png")

        # 击打图片
        self.hit_images.append(img1)
        self.hit_images.append(img2)
        self.hit_images.append(img3)
        self.hit_images.append(img4)
        self.hit_images.append(img5)
        self.hit_images.append(img6)

        # 正常图片
        self.normal_images = self.destroy_images[0:2]

        self.current_image = self.normal_images[0]


class Boss(EnemyThree):
    def __init__(self):
        self.can_shoot = False
        super().__init__()
        self.hurt = 1000
        self.hp = 300
        self.x_speed = 4
        self.direction = 1

    def load_resources(self):

        # 音效  需要更改
        self.destroy_music = pygame.mixer.Sound("../music/enemy3_down.wav")
        self.destroy_music.set_volume(0.05)

        # 坠毁
        for i in range(1, 14):
            img = pygame.image.load("../images/boss"+str(i)+".png")
            self.destroy_images.append(img)

        # 击中
        for i in range(1, 6):
            img = pygame.image.load("../images/boss" + str(i) + ".png")
            self.hit_images.append(img)
        img4 = pygame.image.load("../images/boss4.png")
        img3 = pygame.image.load("../images/boss3.png")
        img2 = pygame.image.load("../images/boss2.png")

        self.hit_images.append(img4)
        self.hit_images.append(img3)
        self.hit_images.append(img2)

        # 普通
        self.normal_images = self.destroy_images[0:1]

        self.current_image = self.normal_images[0]

    def update_position(self):
        # 横向边界反弹
        if self.x <= 0 or self.x + self.get_width() >= 510:
            self.direction = - self.direction

        self.x = self.x + (self.x_speed * self.direction)

        # 纵向移动
        if self.y <= 10:
            self.y += self.y_speed
        else:
            if not self.can_shoot:
                self.can_shoot = True
