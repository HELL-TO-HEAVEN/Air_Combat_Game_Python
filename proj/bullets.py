import pygame
from proj.flyingObject import FlyingObject


class HeroBulletOne(FlyingObject):
    """单线攻击 火焰"""
    def __init__(self, hero):
        super().__init__()
        self.hero = hero
        self.hurt = 2
        self.y_speed = 15
        self.normal_images = []
        self.normal_count = 0
        self.load_resources()

    def load_resources(self):
        # 普通状态
        for i in range(1, 3):
            img = pygame.image.load("../images/pugong" + str(i) + ".png")
            self.normal_images.append(img)
        self.current_image = self.normal_images[0]
        self.x = self.hero.x + self.hero.get_width()/2 - self.get_width()/2
        self.y = self.hero.y

    def update_image(self, normal_rate=2):
        self.normal_count += 1
        index = self.normal_count // normal_rate
        if self.normal_count == normal_rate * len(self.normal_images):
            self.normal_count = 0
            index = 0
        self.current_image = self.normal_images[index]

    def update_position(self):
        self.y -= self.y_speed


class HeroBulletTwo(HeroBulletOne):
    """单线攻击  剑"""
    def __init__(self, hero):
        super().__init__(hero)

    def load_resources(self):
        img = pygame.image.load("../images/pugong5.png")
        self.normal_images.append(img)
        self.current_image = self.normal_images[0]
        self.x = self.hero.x + self.hero.get_width() / 2 - self.get_width() / 2
        self.y = self.hero.y

    def update_image(self, normal_rate=2):
        pass


class HeroBulletThree(HeroBulletTwo):
    """斜向攻击 两侧 红色子弹"""
    def __init__(self, hero, direction):
        self.direction = direction
        self.x_speed = 8
        super().__init__(hero)

    def load_resources(self):
        img = pygame.image.load("../images/bullet.png")
        self.current_image = img
        if self.direction == -1:
            self.x = self.hero.x + self.hero.get_width()/4 - self.get_width()/2
        else:
            self.x = self.hero.x + self.hero.get_width() * 3/4 - self.get_width()/2
        self.y = self.hero.y

    def update_position(self):
        super().update_position()
        self.x += (self.x_speed * self.direction)


class HeroBulletFour(HeroBulletThree):
    """先斜向 再直行 蓝色子弹"""
    def __init__(self, hero, direction):
        super().__init__(hero, direction)
        self.x_speed = 17
        self.x_count = 0

    def load_resources(self):
        img = pygame.image.load("../images/double.png")
        self.current_image = img
        if self.direction == -1:
            self.x = self.hero.x - self.get_width()/2
        else:
            self.x = self.hero.x + self.hero.get_width() - self.get_width()/2
        self.y = self.hero.y

    def update_position(self):
        if self.x_count <= 6:
            self.x_count += 1
            super().update_position()
        else:
            self.y -= self.y_speed


class HeroBulletFive(HeroBulletFour):
    """紫色大招子弹"""
    def __init__(self, hero, direction):
        super().__init__(hero, direction)
        self.x_speed = 17
        self.y_speed = 15

    def load_resources(self):
        img = pygame.image.load("../images/pugong3.png")
        self.current_image = img
        self.x = self.hero.x + self.hero.get_width()/2 - self.get_width()/2
        self.y = self.hero.y

    # 反复变向
    def update_position(self):
        if self.x_count == 154:
            self.x_count = 0

        self.x_count += 1
        self.y -= self.y_speed

        if self.x_count in [4, 13, 28, 50, 80, 119]:    # 4  -5  6  -7  8  -9  : 4  9  15  22 30 39
            self.direction = - self.direction

        self.x += self.x_speed * self.direction


class HeroMissileOne(HeroBulletOne):
    """英雄导弹一"""
    def __init__(self, hero, direction):
        self.direction = direction
        self.hit_images = []
        super().__init__(hero)
        self.x_speed = 2
        self.y_speed = 15
        self.hp = 1
        self.hit_count = 0
        self.position_count = 0
        self.be_hit = False

    def load_resources(self):
        for i in range(1, 5):
            img = pygame.image.load("../images/daodan1"+str(i)+".png")
            self.normal_images.append(img)
        img5 = self.normal_images[2]
        img6 = self.normal_images[1]
        self.normal_images.append(img5)
        self.normal_images.append(img6)

        img_hit = pygame.image.load("../images/daodan_hit.png")
        self.hit_images.append(img_hit)
        self.current_image = self.normal_images[0]

        x1 = self.hero.x
        x2 = self.hero.x + self.hero.get_width() - self.get_width()
        y = self.hero.y - 10
        if self.direction == -1:
            self.x = x1
        else:
            self.x = x2
        self.y = y

    def update_image(self, normal_rate=2, hit_rate=2, destroy_rate=2):
        if self.be_hit:
            self.hit_count += 1
            index = self.hit_count // hit_rate
            if index < len(self.hit_images):
                self.current_image = self.hit_images[index]
            else:
                self.hit_count = 0
                self.be_hit = False

        elif self.hp > 0:
            super().update_image()

    def update_position(self):
        self.position_count += 1

        if self.direction == -1:
            x = self.hero.x
        else:
            x = self.hero.x + self.hero.get_width() - self.get_width()
        y = self.hero.y - 10

        # 前30帧  静止
        if self.position_count < 50:
            self.x = x
            self.y = y
        # 30帧到65帧 ，水平方向 做速度为2 的匀速运动
        elif 50 <= self.position_count <= 85:
            t = self.position_count - 50
            s = self.x_speed * t * self.direction
            self.x = x + s

        #  30帧之后，竖直方向做初速度为 15，加速度为1的匀变速直线运动
        if 50 < self.position_count:
            a = - 1
            t = self.position_count - 50
            current_speed = self.y_speed + a * t
            s = (current_speed**2 - self.y_speed**2) / (2*a)
            self.y = y + s


class HeroMissileTwo(HeroMissileOne):
    """英雄导弹二"""
    def __init__(self, direction, hero):
        super().__init__(direction, hero)
        self.x_speed = 3

    def update_position(self):

        self.position_count += 1

        if self.direction == -1:
            x = self.hero.x
        else:
            x = self.hero.x + self.hero.get_width() - self.get_width()
        y = self.hero.y - 10

        # 前20帧  静止
        if self.position_count < 42:
            self.x = x
            self.y = y

        # 20帧到55帧 ，水平方向做速度为 4 的匀速运动
        elif 42 <= self.position_count <= 82:
            t = self.position_count - 42
            s = self.x_speed * t * self.direction
            self.x = x + s

        #  20帧之后，竖直方向做初速度为 10，加速度为1的匀变速直线运动
        if 42 < self.position_count:
            a = - 1
            t = self.position_count - 42
            current_speed = self.y_speed + a * t
            s = (current_speed**2 - self.y_speed**2) / (2*a)
            self.y = y + s


class BossBullet(FlyingObject):
    """Boss导弹"""
    def __init__(self, boss, direction, pos):
        super().__init__()
        self.direction = direction
        self.pos = pos
        self.boss = boss

        self.hp = 50
        self.hurt = 5
        self.y_speed = 2
        self.x_speed = 2
        self.normal_images = []
        self.hit_images = []
        self.destroy_images = []
        self.normal_count = 0
        self.hit_count = 0
        self.destroy_count = 0
        self.position_count = 0

        self.be_hit = False

        self.load_resources()

    def load_resources(self):
        # 坠毁
        for i in range(1, 10):
            img = pygame.image.load("../images/bossBullet"+str(i)+".png")
            self.destroy_images.append(img)

        # 击中
        self.hit_images.append(self.destroy_images[0])
        img = pygame.image.load("../images/bossBullet_hit.png")
        self.hit_images.append(img)

        # 平常
        self.normal_images.append(self.destroy_images[0])

        self.current_image = self.normal_images[0]
        if self.pos == 1:
            self.x = self.boss.x + 1 / 8 * self.boss.get_width() - self.get_width()/2
        elif self.pos == 2:
            self.x = self.boss.x + 3 / 8 * self.boss.get_width() - self.get_width()/2
        elif self.pos == 3:
            self.x = self.boss.x + 5 / 8 * self.boss.get_width() - self.get_width()/2
        elif self.pos == 4:
            self.x = self.boss.x + 7 / 8 * self.boss.get_width() - self.get_width()/2

        self.y = self.boss.y + self.boss.get_height() - 150

    def update_image(self, normal_rate=2, hit_rate=2, destroy_rate=2):

        if self.hp <= 0:
            self.destroy_count += 1
            index = self.destroy_count // destroy_rate
            if index < len(self.destroy_images):
                self.current_image = self.destroy_images[index]
            else:
                self.can_clear = True

        elif self.be_hit:
            self.hit_count += 1
            index = self.hit_count // hit_rate
            if index < len(self.hit_images):
                self.current_image = self.hit_images[index]
            else:
                self.hit_count = 0
                self.be_hit = False

        else:
            self.normal_count += 1
            index = self.normal_count // normal_rate
            if index < len(self.normal_images):
                self.current_image = self.normal_images[index]
            else:
                self.normal_count = 0

    def update_position(self):
        self.position_count += 1

        if self.position_count <= 30:
            if self.pos == 1:
                self.x = self.boss.x + 1 / 8 * self.boss.get_width() - self.get_width() / 2
            elif self.pos == 2:
                self.x = self.boss.x + 3 / 8 * self.boss.get_width() - self.get_width() / 2
            elif self.pos == 3:
                self.x = self.boss.x + 5 / 8 * self.boss.get_width() - self.get_width() / 2
            elif self.pos == 4:
                self.x = self.boss.x + 7 / 8 * self.boss.get_width() - self.get_width() / 2

            self.y = self.boss.y + self.boss.get_height() - 150

        else:
            if self.x <= 0 or (self.x + self.get_width()) >= 510:
                self.direction = - self.direction

            self.x += self.direction * self.x_speed
            self.y += self.y_speed

