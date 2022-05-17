import sys
import threading

import pygame
import functions as fc
from rain import Rain
from random import randint
from setting import Settings
from character import Character
from boards import Board
from grass import Grass
from polluted import Polluted
from score import Score
from pygame.sprite import Group
from success import Door
from reports import Reports


class Seva:

    def __init__(self):
        # 初始化
        pygame.init()
        pygame.display.set_caption("Seva")
        self.settings = Settings()
        self.WIDTH = self.settings.screen_width
        self.HEIGHT = self.settings.screen_height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen.fill(self.settings.bg_color)
        self.screen_rect = self.screen.get_rect()
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()

        # 进入与退出选择标志
        self.option_type = 2

        # 当前图片绘制标志
        self.screen_type = 0

        # 主题选择标志
        self.theme_type = 0
        self.theme_read()

        self.door = Door(self)
        self.rains = Group()
        self.character = Character(self)
        self.polluted = Polluted(self)
        self.score = Score(self.screen)
        self.report = Reports(self.screen)

        self.show_report = False
        self.key_number = 1

        self.rains_drop = True
        self.rain_height = 0

        self.grasses1 = Group()
        self.grasses1.add(Grass(self.screen, 1000, 460))
        self.grasses1.add(Grass(self.screen, 100, 160))
        self.grasses1.add(Grass(self.screen, 1150, 675))
        self.grasses1.add(Grass(self.screen, 100, 675))
        self.grasses1.add(Grass(self.screen, 150, 675))
        self.grasses1.add(Grass(self.screen, 200, 675))

        self.grasses2 = Group()
        self.grasses2.add(Grass(self.screen, 800, 400))

        self.boards1 = [Board(self.screen, 100, 40, 1000, 500),
                        Board(self.screen, 40, 40, 600, 500),
                        Board(self.screen, 200, 20, 650, 600),
                        Board(self.screen, 200, 40, 300, 380),
                        Board(self.screen, 200, 40, 80, 200),
                        Board(self.screen, 150, 45, 650, 200),
                        Board(self.screen, 200, 50, 1000, 100)]

        self.boards2 = [Board(self.screen, 300, 20, 800, 600),
                        Board(self.screen, 100, 40, 500, 550),
                        Board(self.screen, 50, 20, 900, 250),
                        # 炸弹右
                        Board(self.screen, 30, 10, 250, 450),
                        # 炸弹左
                        Board(self.screen, 80, 10, 170, 450, True),
                        Board(self.screen, 250, 20, 500, 350),
                        Board(self.screen, 200, 40, 1000, 100),
                        Board(self.screen, 200, 10, 100, 200)]

        self.boards3 = [Board(self.screen, 150, 40, 800, 600),
                        Board(self.screen, 400, 20, 500, 450),
                        Board(self.screen, 400, 20, 100, 250),
                        Board(self.screen, 100, 40, 650, 170),
                        Board(self.screen, 500, 40, 900, 250),
                        Board(self.screen, 200, 50, 1000, 100)]

        self.boards4 = [Board(self.screen, 400, 30, 450, 600),
                        Board(self.screen, 150, 20, 600, 450),
                        Board(self.screen, 300, 20, 400, 300),
                        Board(self.screen, 100, 10, 300, 170),
                        Board(self.screen, 80, 10, 620, 150),
                        Board(self.screen, 300, 40, 900, 400),
                        Board(self.screen, 200, 50, 1000, 100)]

        self.boards = self.boards1

        self.polluted_up = False

        self.clock = pygame.time.Clock()

        self.t1 = threading.Thread(target=self.threading_body, name='report线程')

    def run_game(self):
        self._create_rain()

        while True:
            self._check_success()
            self._check_events()
            self._character_run()
            self._check_character_rain()
            self._check_character_water()
            self._check_plat()

            # 进入每个关卡的初始页面
            if self.screen_type == 0:
                self._update_screen_main('images/bg' + str(self.theme_type + 1) + '.png')
            elif self.screen_type == 1:
                self._update_screen(self.grasses1, self.boards1)
                self.boards = self.boards1
            elif self.screen_type == 2:
                self._update_screen(self.grasses1, self.boards2)
                self.boards = self.boards2
            elif self.screen_type == 3:
                fc.update_board(self.boards3[0])
                self._update_screen(self.grasses1, self.boards3)
                self.boards = self.boards3
            elif self.screen_type == 4:
                self._update_screen(self.grasses1, self.boards4)
                self.boards = self.boards4

    def _update_screen_main(self, fileload):
        """更新初始选择页面"""
        self.image_bg = pygame.image.load(fileload)
        self.rect_bg = self.image_bg.get_rect()
        self.rect_bg.midbottom = self.screen_rect.midbottom
        self.screen.blit(self.image_bg, self.rect_bg)
        self._update_quit_and_next()

        pygame.display.flip()

    def _update_screen(self, grasses, boards):
        # 需要再绘制背景颜色，不然会有阴影
        self.screen.fill((255, 255, 255))

        self.rains.draw(self.screen)
        self._rain_drop()
        self._check_rain_oracle()
        self.door.show_door()

        self._create_character()
        self._create_ground()
        self._create_brick(boards)
        self._create_grasses(grasses)
        self._update_pulleted()

        pygame.display.flip()

    def _update_quit_and_next(self):
        if self.option_type == 1:
            self.image_quit = pygame.image.load('images/title2.png')
            self.image_next = pygame.image.load('images/title1(un).png')
        elif self.option_type == 2:
            self.image_quit = pygame.image.load('images/title2(un).png')
            self.image_next = pygame.image.load('images/title1.png')

        self.rect_quit = self.image_quit.get_rect()
        self.rect_next = self.image_next.get_rect()

        self.rect_quit.bottomleft = self.screen_rect.midbottom
        self.rect_next.bottomright = self.screen_rect.bottomright

        self.screen.blit(self.image_quit, self.rect_quit)
        self.screen.blit(self.image_next, self.rect_next)

    def _character_run(self):
        """更改角色跑步图片"""
        if not self.character.jump:
            if self.character.character_type == 2:
                self.character.character_type = 3
                self.character.update_character()
            elif self.character.character_type == 3:
                self.character.character_type = 2
                self.character.update_character()
            if self.character.character_type == 5:
                self.character.character_type = 6
                self.character.update_character()
            elif self.character.character_type == 6:
                self.character.character_type = 5
                self.character.update_character()

    def _check_events(self):
        """监测事件：key按下与否"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.theme_save()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        # 暂停跑动
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
            self.character.character_type = 1
            self.character.update_character()

        if event.key == pygame.K_LEFT:
            self.character.moving_left = False
            self.character.character_type = 4
            self.character.update_character()

        if pygame.key.name(event.key).isdigit():
            n = int(pygame.key.name(event.key))
            if n == 0:
                self.key_number = 10
            else:
                self.key_number = n
            self.show_report = False

    def _check_keydown_events(self, event):
        # 左右跑动
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
            self.character.character_type = 2
            self.character.update_character()
            self.option_type = 2
        elif event.key == pygame.K_LEFT:
            self.character.moving_left = True
            self.character.character_type = 5
            self.character.update_character()
            self.option_type = 1

        # 回车确认
        if event.key == pygame.K_RETURN:
            if self.option_type == 1:
                self.theme_save()
                sys.exit()
            elif self.option_type == 2:
                self.screen_type = self.theme_type + 1

        # 空格跳跃
        if event.key == pygame.K_SPACE:
            self.character.jump = True

        # 1-9控制
        if str(pygame.key.name(event.key)).isdigit():
            self.show_report = True

        # esc退出
        if event.key == pygame.K_ESCAPE:
            sys.exit()

        # R重新开始游戏
        if event.key == pygame.K_r:
            self.theme_type = 0
            self.theme_save()

    def _update_pulleted(self):
        """管理废水的方法"""
        self.screen.blit(self.polluted.image, self.polluted.rect)
        if self.polluted_up:
            if self.polluted.rect.y >= self.screen_rect.top + 50:
                self.polluted.rect.y -= self.settings.polluted_speed

    def _create_rain(self):
        """判断行列有多少元素,设置间距,生产雨添加到Group组"""
        new_rain = Rain(self)
        self.rain_height = new_rain.rect_height
        m = 0
        for x in range(4):
            m += 250
            new_rain = Rain(self)
            random_number = randint(-100, 100)
            new_rain.rect.x = m + random_number
            self.rains.add(new_rain)

    def _create_brick(self, boards):
        """创建游戏界面的木板"""
        for board in boards:
            board.draw_boards(board)

    def _create_grasses(self, grasses):
        """更新花花和分数"""
        for grass in grasses:
            # 是否得到
            self._check_grass_gain(grass)
        # 更新小草数目
        self.score.prep_score()
        # 遍历grasses刷新
        fc.update_grasses(grasses)
        self.score.show_score()

    def _create_character(self):
        """生成人物"""
        self.character.draw_character()
        self.character.move_character()
        self.character.jump_up_character()

    def _create_ground(self):
        """绘制地面"""
        self.image_ground = pygame.image.load('images/ground.png')
        self.rect_ground = self.image_ground.get_rect()
        self.rect_ground.midbottom = self.screen_rect.midbottom
        self.screen.blit(self.image_ground, self.rect_ground)

    def _rain_drop(self):
        # 更新雨下落的Y轴位置
        for read_rain in self.rains.sprites():

            read_rain.rect.y += self.settings.rain_speed
            if read_rain.rect.y >= 150:
                self.rains_drop = True
            else:
                self.rains_drop = False

    def _check_rain_oracle(self):
        # 检查是否到达边界，删除到达边界的元素
        for read_rain in self.rains.copy():
            if read_rain.rect.bottom >= self.screen_height:
                self.rains.remove(read_rain)
                self.polluted_up = True

        if self.rains_drop:
            self._create_rain()

    def _check_grass_gain(self, grass):
        """检测人物是否获得某个花花"""
        collisions = pygame.sprite.spritecollide(self.character, self.grasses1, True)
        if collisions:
            # 大于3减少3棵草（兑换心）
            if self.score.grass_score >= 2:
                self.score.grass_score -= 2
                self.score.heart_score += 1
            else:
                self.score.grass_score += 1

    def _check_character_rain(self):
        """检测雨滴和人物是否碰撞"""
        collision = pygame.sprite.spritecollide(self.character, self.rains, True)  # 第三个参数用来确定是否删除
        if collision:
            if self.score.heart_score == 1:
                self.show_go_screen()
            else:
                self.score.heart_score -= 1
                self.score.prep_score()

    def _check_character_water(self):
        """检测污水和人物是否碰撞"""
        if self.character.rect.top > self.polluted.rect.top + 100:
            self.show_go_screen()

    def _check_plat(self):
        collision = pygame.sprite.spritecollide(self.character, self.boards, False)
        if collision:
            self.character.down = False
            self.settings.character_jump_down = 0
            for c in collision:
                if self.character.rect.top > c.rect.y:
                    self.character.jump = False
                    self.character.down = True
                elif self.character.rect.bottom > c.rect.top and not self.character.jump:
                    self.settings.character_jump_up = 20
            for board in collision:
                if board == self.boards2[4]:
                    board.if_explode = True
        else:
            self.character.down = True

    # 通关判断
    def _check_success(self):
        collision = pygame.sprite.collide_rect(self.character, self.door)
        if collision:
            if self.theme_type < 3:
                self.theme_type += 1
                self.theme_save()
                self.game_pass()
                self.__init__()
            elif self.theme_type == 3:
                self.game_pass()
                self.show_reports()

    def theme_save(self):
        file = open('theme.txt', 'w')
        file.write(str(self.theme_type))
        file.close()

    def theme_read(self):
        file = open('theme.txt', 'r')
        self.theme_type = int(file.read())
        file.close()

    # 开启新线程
    def threading_body(self):
        self.report.prep_text()
        self.report.index = self.key_number
        self.report.show_text(self.key_number)

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_go_screen(self):
        """游戏失败"""
        self.screen.fill((192, 192, 192))
        self.draw_text("GAME OVER", 72, self.settings.bg_color, self.WIDTH / 2, self.HEIGHT / 4)
        self.draw_text("Press a key to play again", 48, self.settings.bg_color, self.WIDTH / 2, self.HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()
        self.__init__()

    def game_pass(self):
        """通过本关卡页面"""
        self.screen.fill((192, 192, 192))
        self.draw_text("CONGRATULATION!", 72, self.settings.bg_color, self.WIDTH / 2, self.HEIGHT / 4)
        self.draw_text("Press a number key to check report!", 48, self.settings.bg_color, self.WIDTH / 2, self.HEIGHT / 2)
        pygame.display.flip()
        self.wait_for_key()

    def show_reports(self):
        """游戏全部通关后可以显示"""
        while True:
            self.screen.fill((255, 255, 255))
            if self.show_report:
                if not self.t1.is_alive() and len(self.report.text) == 0:
                    self.t1.start()
                else:
                    print(self.key_number)
                    self.report.show_text(self.key_number)
            self._check_events()
            pygame.display.flip()


if __name__ == '__main__':
    seva = Seva()
    seva.run_game()
