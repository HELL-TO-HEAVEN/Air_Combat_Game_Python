import sys
from pygame.locals import *
from proj.enemys import *
from proj.hero import *
from proj.shield import Shield
from proj.ultimateSkill import UltimateSkill


class AirCombatGame:
    """飞机大战"""
    # 游戏状态
    READY = 1           # 游戏准备中
    PLAYING = 2         # 游戏进行中
    OVER = 3            # 游戏结束
    status = READY      # 初始状态为游戏准备中
    frame = 0           # 播放帧数
    screen = None       # 游戏窗口
    X_SIZE = 510        # 窗口宽度
    Y_SIZE = 760        # 窗口高度
    enemies = []        # 敌机祖
    hero_bullets = []   # 英雄子弹组
    rewards = []        # 补给组
    enemy_bullets = []  # 敌机子弹组
    our_hero = None     # 英雄机
    shield = None       # 护罩
    is_ultimate_skill = False  # 终极技能释放状态
    ultimate_skill = None  # 终极技能
    background = None       # 背景图片
    bg_y_one = 0            # 第一张背景图片的纵坐标
    bg_y_two = 0            # 第二张背景图片的纵坐标
    image_over = None       # 结束时显示的图片
    bgm = None              # 背景音乐
    has_boss = False        # 当前有没有boss
    boss_count = 0          # 当boss被消灭时 开始计时

    @classmethod
    def load_resources(cls):
        cls.image_over = pygame.image.load('../images/gameover.png')
        cls.background = pygame.image.load("../images/background.png")
        cls.bgm = pygame.mixer.music.load("../music/bgm.mp3")

    @classmethod
    def create_objects(cls):
        """生产各种"""
        # 生产敌机
        if cls.frame % 15 == 0:
            e = EnemyOne()
            e.x = random.randint(0, cls.X_SIZE - e.get_width())
            e.y = - e.get_height()
            cls.enemies.append(e)

        if cls.frame % 20 == 0:
            e = EnemyTwo()
            e.x = random.randint(0, cls.X_SIZE - e.get_width())
            e.y = - e.get_height()
            cls.enemies.append(e)

        if cls.frame % 30 == 0:
            e = EnemyThree()
            e.x = random.randint(0, cls.X_SIZE - e.get_width())
            e.y = - e.get_height()
            cls.enemies.append(e)

        # 生产Boss
        for each in cls.enemies:
            cls.has_boss = False
            if isinstance(each, Boss):
                cls.has_boss = True
                break

        if not cls.has_boss:
            cls.boss_count += 1

        if cls.boss_count == 200:
            cls.boss_count = 0
            boss = Boss()
            boss.x = random.randint(0, cls.X_SIZE - boss.get_width())
            boss.y = - boss.get_height() - 10
            cls.enemies.append(boss)

        # 生产Boss导弹
        if cls.frame % 100 == 0:
            for each in cls.enemies:
                if isinstance(each, Boss) and each.can_shoot:
                    b1 = BossBullet(each, 1, 1)
                    b2 = BossBullet(each, -1, 2)
                    b3 = BossBullet(each, 1, 3)
                    b4 = BossBullet(each, -1, 4)
                    cls.enemy_bullets.extend([b1, b2, b3, b4])

        # 生产英雄子弹
        if cls.frame % 3 == 0:
            # 斜向子弹
            cls.hero_bullets.append(HeroBulletThree(cls.our_hero, 1))
            cls.hero_bullets.append(HeroBulletThree(cls.our_hero, -1))
            # 斜向直向
            cls.hero_bullets.append(HeroBulletFour(cls.our_hero, 1))
            cls.hero_bullets.append(HeroBulletFour(cls.our_hero, -1))

            # 英雄大招子弹
            if cls.is_ultimate_skill:
                # 宝剑子弹
                cls.hero_bullets.append(HeroBulletTwo(cls.our_hero))
                # 紫色子弹
                cls.hero_bullets.append(HeroBulletFive(cls.our_hero, 1))
                cls.hero_bullets.append(HeroBulletFive(cls.our_hero, -1))
            else:
                # 火线子弹
                cls.hero_bullets.append(HeroBulletOne(cls.our_hero))

        # 生产英雄导弹
        if cls.frame % 200 == 0:
            cls.hero_bullets.append(HeroMissileOne(cls.our_hero, -1))
            cls.hero_bullets.append(HeroMissileOne(cls.our_hero, 1))
            cls.hero_bullets.append(HeroMissileTwo(cls.our_hero, -1))
            cls.hero_bullets.append(HeroMissileTwo(cls.our_hero, 1))

        # 生产补给
        for each in cls.enemies:
            if each.destroy_count == 1:
                variable = random.random()
                if variable <= 0.5:
                    if isinstance(each, EnemyOne):
                        star = each.shoot_reward_star(6)
                        if star:
                            cls.rewards.append(star)
                    if isinstance(each, EnemyTwo):
                        star = each.shoot_reward_star(12)
                        if star:
                            cls.rewards.append(star)
                    if isinstance(each, EnemyThree):
                        star = each.shoot_reward_star(24)
                        if star:
                            cls.rewards.append(star)
                    if isinstance(each, Boss):
                        star = each.shoot_reward_star(100)
                        if star:
                            cls.rewards.append(star)
                else:
                    if isinstance(each, EnemyOne):
                        life = each.shoot_reward_life(4)
                        if life:
                            cls.rewards.append(life)
                    if isinstance(each, EnemyTwo):
                        life = each.shoot_reward_life(7)
                        if life:
                            cls.rewards.append(life)
                    if isinstance(each, EnemyThree):
                        life = each.shoot_reward_life(10)
                        if life:
                            cls.rewards.append(life)
                    if isinstance(each, Boss):
                        life = each.shoot_reward_life(100)
                        if life:
                            cls.rewards.append(life)

    @classmethod
    def collision_detection(cls):
        """碰撞检测"""
        # 判断英雄和补给碰撞
        for each in cls.rewards:
            is_collision = Rect.colliderect(each.get_rect(), cls.our_hero.get_rect())
            if is_collision and isinstance(each, RewardOne):
                each.can_clear = True
                current_mp = cls.our_hero.mp + each.value
                if current_mp >= cls.our_hero.max_mp:
                    cls.our_hero.mp = cls.our_hero.max_mp
                else:
                    cls.our_hero.mp = current_mp
            if is_collision and isinstance(each, RewardTwo):
                each.can_clear = True
                current_hp = cls.our_hero.hp + each.value
                if current_hp >= cls.our_hero.max_hp:
                    cls.our_hero.hp = cls.our_hero.max_hp
                else:
                    cls.our_hero.hp = current_hp

        # 判断英雄和敌机子弹碰撞
        for each in cls.enemy_bullets:
            is_collision = Rect.colliderect(each.get_rect(), cls.our_hero.get_rect())
            # 导弹
            if is_collision and isinstance(each, BossBullet):
                if each.hp > 0:
                    current_hp = cls.our_hero.hp - each.hurt
                    if current_hp <= 0:
                        cls.our_hero.hp = 0
                    else:
                        cls.our_hero.hp = current_hp
                    each.hp = 0
            # 普通敌机子弹
            elif is_collision:
                current_hp = cls.our_hero.hp - each.hurt
                if current_hp <= 0:
                    cls.our_hero.hp = 0
                else:
                    cls.our_hero.hp = current_hp
                each.can_clear = True

        # 判断英雄和敌机碰撞
        for each in cls.enemies:
            is_collision = Rect.colliderect(each.get_rect(), cls.our_hero.get_rect())
            if is_collision and each.hp > 0:
                cls.our_hero.be_hit = True
                current_hp = cls.our_hero.hp - each.hurt
                if current_hp <= 0:
                    cls.our_hero.hp = 0
                else:
                    cls.our_hero.hp = current_hp
                each.hp = 0

        # 英雄子弹和敌机碰撞
        for each_bullet in cls.hero_bullets:
            for each_enemy in cls.enemies:
                is_collision = Rect.colliderect(each_enemy.get_rect(), each_bullet.get_rect())
                if is_collision and each_enemy.hp > 0:
                    each_bullet.can_clear = True
                    each_enemy.be_hit = True
                    each_enemy.hp -= each_bullet.hurt

        # 判断英雄子弹和Boss导弹碰撞：

        for each_enemy_bullet in cls.enemy_bullets:
            if isinstance(each_enemy_bullet, BossBullet):
                for each_hero_bullet in cls.hero_bullets:
                    is_collision = Rect.colliderect(each_enemy_bullet.get_rect(), each_hero_bullet.get_rect())
                    if is_collision and each_enemy_bullet.hp > 0:
                        each_enemy_bullet.be_hit = True
                        each_enemy_bullet.hp -= each_hero_bullet.hurt
                        each_hero_bullet.can_clear = True

        # 判断大招和敌机碰撞
        if cls.is_ultimate_skill:
            for each in cls.enemies:
                is_collision = Rect.colliderect(each.get_rect(), cls.ultimate_skill.get_rect())
                if is_collision:
                    if isinstance(each, Boss):
                        each.hp -= cls.ultimate_skill.hurt
                    else:
                        each.hp = 0

        # 判断大招和Boss导弹碰撞
        if cls.is_ultimate_skill:
            for each in cls.enemy_bullets:
                if isinstance(each, BossBullet):
                    is_collision = Rect.colliderect(each.get_rect(), cls.ultimate_skill.get_rect())
                    if is_collision:
                        each.hp = 0

    '''越界检测'''
    @classmethod
    def boundary_detection(cls):
        # 检测越界英雄子弹
        for each in cls.hero_bullets:
            if each.x < - 100 or each.x > 100 + cls.X_SIZE or each.y < - each.get_height():
                each.can_clear = True

        # 检测越界敌机子弹
        for each in cls.enemy_bullets:
            if each.y > cls.Y_SIZE:
                each.can_clear = True

        # 检测越界敌机
        for each in cls.enemies:
            if each.y > cls.Y_SIZE:
                each.can_clear = True

        # 检测越界补给
        for each in cls.rewards:
            if each.y > cls.Y_SIZE:
                each.can_clear = True

    '''删除各种'''
    @classmethod
    def clear_all(cls):
        # 消耗mp
        if cls.is_ultimate_skill:
            cls.our_hero.mp -= 1
            if cls.our_hero.mp == 0:
                cls.is_ultimate_skill = False

        # 删除补给
        temp = filter(lambda x: False if x.can_clear else True, cls.rewards)
        cls.rewards = list(temp)
        # 删除敌机
        temp = filter(lambda x: False if x.can_clear else True, cls.enemies)
        cls.enemies = list(temp)
        # 删除敌机子弹
        temp = filter(lambda x: False if x.can_clear else True, cls.enemy_bullets)
        cls.enemy_bullets = list(temp)
        # 删除英雄子弹
        temp = filter(lambda x: False if x.can_clear else True, cls.hero_bullets)
        cls.hero_bullets = list(temp)

    '''更新位置'''
    @classmethod
    def update_position_all(cls):
        # 更新 补给 敌机 子弹 英雄 的位置
        all_list = cls.rewards + cls.enemies + cls.enemy_bullets + cls.hero_bullets
        for each in all_list:
            each.update_position()

        # 更新大招位置
        if cls.is_ultimate_skill:
            cls.ultimate_skill.update_position()
        # 更新护盾位置
        if cls.is_ultimate_skill or cls.our_hero.be_hit:
            cls.shield.update_position()

        # 更新英雄机位置
        x, y = pygame.mouse.get_pos()
        x -= cls.our_hero.get_width()/2
        y -= cls.our_hero.get_height()/2
        cls.our_hero.move_to(x, y)

    '''更新画面'''
    @classmethod
    def update_image_all(cls):

        # 更新补给，敌机，低级子弹，英雄子弹 的画面
        all_list = cls.rewards + cls.enemies + cls.enemy_bullets + cls.hero_bullets
        all_list.append(cls.our_hero)
        for each in all_list:
            each.update_image()

        # 更新护盾画面
        if cls.is_ultimate_skill or cls.our_hero.be_hit:
            cls.shield.update_image()

        # 大招更新image_rect
        if cls.is_ultimate_skill:
            cls.ultimate_skill.update_image_rect()

    '''画血条蓝条'''
    @classmethod
    def draw_hero_value(cls):
        # 画血条蓝条
        hp = 0
        mp = 0
        hp_percent = 0
        mp_percent = 0

        if cls.our_hero.hp >= 0:
            hp = cls.our_hero.hp
            hp_percent = hp / cls.our_hero.max_hp
        if cls.our_hero.mp >= 0:
            mp = cls.our_hero.mp
            mp_percent = mp / cls.our_hero.max_mp

        frame_width = 150
        frame_height = 14
        thickness = 3
        # hp外框
        pygame.draw.rect(cls.screen, [200, 200, 200], [30, 710, frame_width, frame_height], thickness)
        # mp外框
        pygame.draw.rect(cls.screen, [200, 200, 200], [30, 730, frame_width, frame_height], thickness)

        width_max = frame_width - 2 * thickness
        height_max = frame_height - 2 * thickness
        hp_width = width_max * hp_percent
        mp_width = width_max * mp_percent
        # hp红条
        pygame.draw.rect(cls.screen, [238, 99, 99], [30 + thickness, 710 + thickness, hp_width, height_max], 0)
        # mp蓝条
        pygame.draw.rect(cls.screen, [0, 191, 255], [30 + thickness, 730 + thickness, mp_width, height_max], 0)
        # 画数值 百分比
        my_font = pygame.font.SysFont("tempus sans itc", 17)

        hp_text = "HP               " + str(hp) + "/"+str(cls.our_hero.max_hp)
        hp_percent_text = ("%.2f" % (hp_percent * 100)) + "%"
        mp_text = "MP               " + str(mp) + "/"+str(cls.our_hero.max_mp)
        mp_percent_text = ("%.2f" % (mp_percent * 100)) + "%"

        hp_text_surface_one = my_font.render(hp_text, True, (255, 255, 255))
        hp_text_surface_two = my_font.render(hp_percent_text, True, (255, 255, 255))
        mp_text_surface_one = my_font.render(mp_text, True, (255, 255, 255))
        mp_text_surface_two = my_font.render(mp_percent_text, True, (255, 255, 255))

        cls.screen.blit(hp_text_surface_one, (7, 705))
        cls.screen.blit(hp_text_surface_two, (190, 705))
        cls.screen.blit(mp_text_surface_one, (5, 725))
        cls.screen.blit(mp_text_surface_two, (190, 725))

    '''按照顺序画各种'''
    @classmethod
    def draw_all(cls):
        # 画背景
        cls.screen.blit(cls.background, (0, cls.bg_y_one))
        cls.screen.blit(cls.background, (0, cls.bg_y_two))

        # 画大招
        if cls.is_ultimate_skill:
            cls.ultimate_skill.blit_me(cls.screen)
        # 画护盾
        if cls.is_ultimate_skill or cls.our_hero.be_hit:
            cls.shield.blit_me(cls.screen)

        # 画英雄子弹
        for each in cls.hero_bullets:
            each.blit_me(cls.screen)

        # 画英雄
        cls.our_hero.blit_me(cls.screen)

        # 画敌机子弹
        for each in cls.enemy_bullets:
            each.blit_me(cls.screen)

        # 画敌机
        for each in cls.enemies:
            each.blit_me(cls.screen)

        # 画补给
        for each in cls.rewards:
            each.blit_me(cls.screen)

        # 画血条蓝条
        cls.draw_hero_value()

    '''主程序'''
    @classmethod
    def main(cls):
        # 初始化 pygame
        pygame.init()
        pygame.display.set_caption("Air—Combat Game!")
        # 得到窗口 获得一个窗口对象
        cls.screen = pygame.display.set_mode((cls.X_SIZE, cls.Y_SIZE), pygame.RESIZABLE, 32)

        # 加载资源
        cls.load_resources()

        # 时钟对象
        clock = pygame.time.Clock()

        # 游戏主循环
        # 1 处理游戏事件 2 更新游戏状态 3.

        # 单曲循环背景音乐
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.05)

        # 初始英雄 大招 盾牌
        cls.our_hero = Hero()
        cls.our_hero.move_to(200, 500)
        cls.ultimate_skill = UltimateSkill(cls.our_hero, 120, 865, 123)
        cls.shield = Shield(cls.our_hero)

        while True:
            # 判断游戏是否结束
            if cls.our_hero.hp <= 0:
                cls.status = cls.OVER

            clock.tick(60)

            # 帧数
            cls.frame += 1
            if cls.frame == 1000:
                cls.frame = 0

            '''事件'''
            for event in pygame.event.get():

                # 如果关闭 程序退出
                if event.type == pygame.QUIT:
                    sys.exit()

                # 鼠标单击事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if cls.status == cls.READY:
                        cls.status = cls.PLAYING
                    elif cls.status == cls.OVER:
                        cls.status = cls.READY

                # 键盘按键事件
                if event.type == pygame.KEYDOWN and cls.status == cls.PLAYING:
                    key_down = event.key
                    # 如果按空格键 大招开启
                    if key_down == K_SPACE and cls.our_hero.mp > 0:
                        cls.is_ultimate_skill = True

            if cls.status == cls.OVER:
                pass

            elif cls.status == cls.READY:
                cls.frame = 0    # 帧数清0
                cls.enemies = []  # 敌机祖
                cls.hero_bullets = []  # 英雄子弹组
                cls.rewards = []  # 补给组
                cls.enemy_bullets = []  # 敌机子弹组
                cls.bosses = []  # boss组
                # 英雄机满血满状态复活
                cls.our_hero.hp = cls.our_hero.max_hp
                cls.our_hero.mp = cls.our_hero.max_mp
                cls.our_hero.move_to(200, 500)

                # 初始背景图片位置
                cls.bg_y_one = - cls.background.get_height()
                cls.bg_y_two = 0

                # 大招关闭
                cls.is_ultimate_skill = False

            # 如果程序运行中
            elif cls.status == cls.PLAYING:
                cls.bg_y_one += 10
                cls.bg_y_two += 10
                if cls.bg_y_one >= 760:
                    cls.bg_y_one -= 2*cls.background.get_height()
                if cls.bg_y_two >= 760:
                    cls.bg_y_two -= 2 * cls.background.get_height()

                cls.collision_detection()  # 碰撞检测
                cls.boundary_detection()  # 边界检测
                cls.clear_all()                 # 删除对象
                cls.create_objects()            # 产生对象
                if cls.frame % 2 == 0:
                    cls.update_position_all()  # 更新所有对象位置

            cls.update_image_all()  # 更新对象动画
            cls.draw_all()  # 绘画图层
            # 如果结束状态，绘制结束图片
            if cls.status == cls.OVER:
                cls.screen.blit(cls.image_over, (0, 0))

            pygame.display.flip()  # 图像显示


if __name__ == "__main__":
    AirCombatGame.main()
