import os
import sys
from random import choice

import pygame
import pytmx

pygame.init()
Timer_Spider_TYPE = 10
WINDOW_SIZE = WIDTH, HEIGTH = 2732, 1536
SCALE = 10
fps = 20
ALPHA = 180
BOARD = []

all_sprites = pygame.sprite.Group()
all_sprites_mini = pygame.sprite.Group()
spider_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
object_sprites = pygame.sprite.Group()


def load_image(name, anime):
    full_name = f'data/image/{anime}/{name}'
    if not os.path.isfile(full_name):
        sys.exit()
    image = pygame.image.load(full_name)

    return image


class Board:

    def __init__(self):
        self.map = pytmx.load_pygame('data/board/map.tmx')
        self.width = self.map.width
        self.hegth = self.map.height
        self.cell_size = self.map.tilewidth
        self.left = 0
        self.top = 0

    def set_view(self, left, top):
        self.left = left
        self.top = top

    def render(self, screen):
        for y in range(self.hegth):
            BOARD.append([])
            for x in range(self.width):
                BOARD[y].append('_')
                image = self.map.get_tile_image(x, y, 0)
                screen_1 = screen
                if image:
                    screen_1.blit(image, (self.left + x * self.cell_size, self.top + y * self.cell_size))
                image_1 = self.map.get_tile_image(x, y, 1)
                if image_1:

                    if self.map.get_tile_gid(x, y, 1) not in [104, 105, 106, 107, 116, 117, 118, 119, 122, 123, 129,
                                                              130, 135, 136, 131, 128, 121, 134, 124, 125, 141, 188,
                                                              189, 205, 206,
                                                              132, 137, 138, 139, 140, 182, 183, 199, 200]:

                        id_tiled = self.map.get_tile_gid(x, y, 1)
                        BOARD[y][x] = id_tiled
                    else:
                        if self.map.get_tile_gid(x, y, 1) in [104, 105, 106, 107, 116, 117]:
                            object_sprites.add(Object_Map(image_1, y, x, self.cell_size))
                    screen_1.blit(image_1, (self.left + x * self.cell_size, self.top + y * self.cell_size))

        for row in BOARD:
            print(row)
        return screen_1

    def get_cell(self, x, y):
        return x // self.cell_size, y // self.cell_size


class Spider(pygame.sprite.Sprite):
    def __init__(self, x, y, v, live, board, vision=150):
        super().__init__(all_sprites)
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.v = v
        self.hp = live
        self.live_max = self.hp
        self.is_atack = False
        self.vision = vision
        self.position()
        self.board = board
        self.delay = 100
        pygame.time.set_timer(Timer_Spider_TYPE, self.delay)

    def position(self):
        self.image_list_0 = [load_image('s_0_0.png', 'spider'), load_image('s_0_1.png', 'spider'),
                             load_image('s_0_2.png', 'spider'), load_image('s_0_3.png', 'spider'),
                             load_image('s_0_4.png', 'spider'), load_image('s_0_5.png', 'spider'),
                             ]
        self.image_list_1 = [load_image('s_1_0.png', 'spider'), load_image('s_1_1.png', 'spider'),
                             load_image('s_1_2.png', 'spider'), load_image('s_1_3.png', 'spider'),
                             load_image('s_1_4.png', 'spider'), load_image('s_1_5.png', 'spider'),
                             ]
        self.image_list_2 = [load_image('s_2_0.png', 'spider'), load_image('s_2_1.png', 'spider'),
                             load_image('s_2_2.png', 'spider'), load_image('s_2_3.png', 'spider'),
                             load_image('s_2_4.png', 'spider'), load_image('s_2_5.png', 'spider'),
                             ]
        self.image_list_3 = [load_image('s_3_0.png', 'spider'), load_image('s_3_1.png', 'spider'),
                             load_image('s_3_2.png', 'spider'), load_image('s_3_3.png', 'spider'),
                             load_image('s_3_4.png', 'spider'), load_image('s_3_5.png', 'spider'),
                             ]
        self.image_h_list = [load_image('s_h_0.png', 'spider'), load_image('s_h_1.png', 'spider'),
                             load_image('s_h_2.png', 'spider'), load_image('s_h_3.png', 'spider')]

        self.image_atacx_x_0 = [load_image('s_a_x_0.png', 'spider'), load_image('s_a_x_1.png', 'spider'),
                                load_image('s_a_x_2.png', 'spider'), load_image('s_a_x_3.png', 'spider')]

        self.image_atacx_x_1 = [load_image('s_a_x1_0.png', 'spider'), load_image('s_a_x1_1.png', 'spider'),
                                load_image('s_a_x1_2.png', 'spider'), load_image('s_a_x1_3.png', 'spider')]

        self.image_atacx_y_0 = [load_image('s_a_y_0.png', 'spider'), load_image('s_a_y_1.png', 'spider'),
                                load_image('s_a_y_2.png', 'spider'), load_image('s_a_y_3.png', 'spider')]

        self.image_atacx_y_1 = [load_image('s_a_y1_0.png', 'spider'), load_image('s_a_y1_1.png', 'spider'),
                                load_image('s_a_y1_2.png', 'spider'), load_image('s_a_y1_3.png', 'spider')]

        self.image = self.image_list_0[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.count = 0
        self.direction = 0
        self.list_direction = [0, 1, 2, 3]

    def update(self):
        self.count += 1
        if self.hp <= 0:

            self.image = self.image_h_list[self.count % 4]
            self.vy = 0
            self.vx = 0

            if self.count > 19:
                spider_group.remove(self)
                self.kill()

        elif self.metod_vision():
            self.metod_atack()

        elif self.direction == 0:
            x, y = self.board.get_cell(self.rect.x + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2 - self.v)
            if BOARD[y][x] == '_':
                self.vy = -self.v
                self.vx = 0
                self.image = self.image_list_0[self.count % 6]
                self.rect = self.rect.move(self.vx, self.vy)
            else:
                self.direction = choice((1, 2, 3))
                self.count = 0

        elif self.direction == 1:
            x, y = self.board.get_cell(self.rect.x + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2 + self.v)
            if BOARD[y][x] == '_':
                self.image = self.image_list_1[self.count % 6]
                self.vy = self.v
                self.vx = 0
                self.rect = self.rect.move(self.vx, self.vy)
            else:
                self.direction = choice((0, 2, 3))
                self.count = 0

        elif self.direction == 2:
            x, y = self.board.get_cell(self.rect.x - self.v + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2)
            if BOARD[y][x] == '_':
                self.vy = 0
                self.vx = -self.v
                self.image = self.image_list_2[self.count % 6]
                self.rect = self.rect.move(self.vx, self.vy)
            else:
                self.direction = choice((0, 1, 3))
                self.count = 0

        elif self.direction == 3:
            x, y = self.board.get_cell(self.rect.x + self.v + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2)
            if BOARD[y][x] == '_':
                self.vy = 0
                self.vx = self.v
                self.image = self.image_list_3[self.count % 6]
                self.rect = self.rect.move(self.vx, self.vy)
            else:
                self.direction = choice((0, 1, 2))
                self.count = 0

        else:
            self.rect.x-=10
            self.rect.y-=10

        if pygame.sprite.spritecollideany(self, hero_group) and hero.is_atack:
            self.hp -= hero.damage
        pygame.draw.rect(self.image, (0, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 0)
        pygame.draw.rect(self.image, (255, 0, 0),
                         (self.image.get_width() // 2 - 10, 0, int((20 / self.live_max) * self.hp), 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 1)
        self.object_protection()

    def object_protection(self):
        if self.count % 20 == 0:
            a = self.list_direction.pop(self.list_direction.index(self.direction))
            self.direction = choice(self.list_direction)
            self.list_direction.append(a)
            self.count = 0

    def metod_vision(self):
        x_1, y_1, r_1 = self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2, self.vision
        x_2, y_2, r_2 = hero.rect.x + hero.rect.width // 2, hero.rect.y + hero.rect.height // 2, hero.rect.width // 2
        l = ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5

        if l <= r_1 + r_2:
            return True
        else:
            return False

    def metod_atack(self):

        x_s = self.rect.x + self.rect.width // 2
        x_h = hero.rect.x + hero.rect.width // 2
        y_s = self.rect.y + self.rect.height // 2
        y_h = hero.rect.y + hero.rect.height // 2
        # print(x_s, x_h, y_s, y_h, self.count)
        if x_s - x_h > 0 and x_s - x_h > 5:
            x, y = self.board.get_cell(self.rect.x - self.v + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2)
            if BOARD[y][x] == '_':
                self.rect.x -= self.v
                self.image = self.image_atacx_x_0[self.count % 4]




        elif x_s - x_h < 0 and x_s - x_h < 5:
            x, y = self.board.get_cell(self.rect.x + self.v + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2)
            if BOARD[y][x] == '_':
                self.rect.x += self.v
                self.image = self.image_atacx_x_1[self.count % 4]

        if y_s - y_h < 0 and y_s - y_h < 5:
            x, y = self.board.get_cell(self.rect.x + self.image.get_width() // 2,
                                       self.rect.y + self.v + self.image.get_height() // 2)
            if BOARD[y][x] == '_':
                self.rect.y += self.v
                self.image = self.image_atacx_y_1[self.count % 4]





        elif y_s - y_h > 0 and y_s - y_h > 5:
            x, y = self.board.get_cell(self.rect.x + self.image.get_width() // 2,
                                       self.rect.y + self.image.get_height() // 2 - self.v)
            if BOARD[y][x] == '_':
                self.rect.y -= self.v
                self.image = self.image_atacx_y_0[self.count % 4]


class MiniHero(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(all_sprites_mini)
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.image = load_image('hero_0_0.png', 'hero')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def update(self):
        self.rect = self.rect.move(self.vx // SCALE, self.vy // SCALE)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.experience = 0
        self.x = x
        self.y = y
        self.vx = 10
        self.vy = 10
        self.damage = 10
        self.move()
        self.atack()
        self.level = 1

    def atack(self):
        self.image_atack_lict = [load_image('hero_a_0.png', 'hero'), load_image('hero_a_1.png', 'hero'),
                                 load_image('hero_a_2.png', 'hero'),
                                 load_image('hero_a_3.png', 'hero'),
                                 load_image('hero_a_4.png', 'hero')]
        self.is_atack = False
        self.count_atack = 0
        self.live = 500
        self.live_max = self.live

    def move(self):
        self.image_list_y_0 = [load_image('hero_0_0.png', 'hero'), load_image('hero_0_1.png', 'hero'),
                               load_image('hero_0_2.png', 'hero'),
                               load_image('hero_0_3.png', 'hero'),
                               load_image('hero_0_4.png', 'hero'), load_image('hero_0_5.png', 'hero')]
        self.image_list_y_1 = [load_image('hero_1_0.png', 'hero'), load_image('hero_1_1.png', 'hero'),
                               load_image('hero_1_2.png', 'hero'),
                               load_image('hero_1_3.png', 'hero'),
                               load_image('hero_1_4.png', 'hero'), load_image('hero_1_5.png', 'hero')]
        self.image_list_x_0 = [load_image('hero_3_0.png', 'hero'), load_image('hero_3_1.png', 'hero'),
                               load_image('hero_3_2.png', 'hero'),
                               load_image('hero_3_3.png', 'hero'),
                               load_image('hero_3_4.png', 'hero'), load_image('hero_3_5.png', 'hero')]
        self.image_list_x_1 = [load_image('hero_2_0.png', 'hero'), load_image('hero_2_1.png', 'hero'),
                               load_image('hero_2_2.png', 'hero'),
                               load_image('hero_2_3.png', 'hero'),
                               load_image('hero_2_4.png', 'hero'), load_image('hero_2_5.png', 'hero')]
        self.image = self.image_list_y_0[0]

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

        self.count_y_1 = 0
        self.is_klav_y_1 = False
        self.count_y_2 = 0
        self.is_klav_y_2 = False
        self.count_x_0 = 0
        self.is_klav_x_0 = False
        self.count_x_1 = 0
        self.is_klav_x_1 = False

    def update(self):
        self.damage = max(self.experience // 10, 10)
        if pygame.sprite.spritecollideany(self, object_sprites):
            self.live = min(self.live + 0.05, self.live_max)
        if self.is_klav_y_2:
            self.image = self.image_list_y_0[self.count_y_2 % 6]
        if self.is_klav_y_1:
            self.image = self.image_list_y_1[self.count_y_1 % 6]
        if self.is_klav_x_0:
            self.image = self.image_list_x_0[self.count_x_0 % 6]
        if self.is_klav_x_1:
            self.image = self.image_list_x_1[self.count_x_1 % 6]
        if self.is_atack:
            self.image = self.image_atack_lict[self.count_atack % 5]

        list_atack = pygame.sprite.spritecollide(self, spider_group, False)
        if list_atack:
            for spider in list_atack:
                if spider.hp > 0:
                    self.live = max(self.live - 1, 0)
                else:
                    self.experience += 1

        pygame.draw.rect(self.image, (0, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 0)
        pygame.draw.rect(self.image, (0, 255, 0),
                         (self.image.get_width() // 2 - 10, 0, (20 * self.live) // self.live_max, 5))
        pygame.draw.rect(self.image, (0, 255, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 1)
        self.mask = pygame.mask.from_surface(self.image)
        self.get_mini(self.image.copy())
        mini_hero.rect.x = self.rect.x // 10
        mini_hero.rect.y = self.rect.y // 10

    def get_mini(self, image_mini):
        mini_hero.image = pygame.transform.scale(image_mini, (12, 16))


class BottomPanel:
    def __init__(self, screen, screen_mini):
        width_line = 10
        pygame.draw.rect(screen, (125, 125, 125),
                         (0, pygame.display.Info().current_h - width_line, pygame.display.Info().current_w, width_line),
                         0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (0, pygame.display.Info().current_h - screen_mini.get_height() - 10, screen_mini.get_width(),
                          width_line), 0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (0, pygame.display.Info().current_h - screen_mini.get_height() - 10, width_line,
                          screen_mini.get_height()), 0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (screen_mini.get_width(), pygame.display.Info().current_h - screen_mini.get_height() - 10,
                          width_line,
                          screen_mini.get_height()), 0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (0, 0,
                          pygame.display.Info().current_w,
                          30), 0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (0, 0, pygame.display.Info().current_w, width_line), 0)
        pygame.draw.rect(screen, (125, 125, 125), (0, 0, width_line, pygame.display.Info().current_h), 0)
        pygame.draw.rect(screen, (125, 125, 125),
                         (pygame.display.Info().current_w - width_line, 0, width_line, pygame.display.Info().current_h),
                         0)

        font = pygame.font.Font(None, 25)
        text_experience = font.render(f'Опыт:{hero.experience}', True, (255, 0, 0))
        screen.blit(text_experience, (30, 10))

        font = pygame.font.Font(None, 25)
        text_damage = font.render(f'Урон:{hero.damage}', True, (0, 255, 0))
        screen.blit(text_damage, (30 + text_experience.get_width() + 30, 10))

        font = pygame.font.Font(None, 25)
        text_level = font.render(f'Уровень:{hero.level}', True, (0, 255, 255))
        screen.blit(text_level, (30 + text_experience.get_width() + 30 + text_damage.get_width() + 30, 10))

        font = pygame.font.Font(None, 25)
        text_hp = font.render(f'Здоровье:{int(hero.live)}', True, (0, 255, 255))
        screen.blit(text_hp, (
            30 + text_experience.get_width() + 30 + text_damage.get_width() + 30 + text_level.get_width() + 30, 10))


class Object_Map(pygame.sprite.Sprite):
    def __init__(self, image, y, x, cell_size):
        super().__init__(object_sprites)
        self.rect = image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size
        self.mask = pygame.mask.from_surface(image)


def handling_mouse_actions(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        click = event.button
        if click == 1:
            hero.is_atack = True

            hero.count_atack += 1
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            hero.is_atack = False
            hero.count_atack = 0
            hero.image = hero.image_atack_lict[0]


def handling_keyboard_actions(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_p:
            sys.exit()
        if event.key == pygame.K_w:
            hero.is_klav_y_1 = True
            # hero.vy = -10


        elif event.key == pygame.K_s:
            hero.is_klav_y_2 = True
            # hero.vy = 10

        if event.key == pygame.K_d:
            # hero.vx = 10
            hero.is_klav_x_0 = True

        elif event.key == pygame.K_a:
            # hero.vx = -10
            hero.is_klav_x_1 = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
            hero.is_klav_y_1 = False
            hero.count_y_1 = 0
            # hero.vy = 0
        if event.key == pygame.K_s:
            hero.is_klav_y_2 = False
            hero.count_y_2 = 0
            # hero.vy = 0
        if event.key == pygame.K_d:
            # hero.vx = 0
            hero.count_x_0 = 0
            hero.is_klav_x_0 = False
        if event.key == pygame.K_a:
            # hero.vx = 0
            hero.count_x_1 = 0
            hero.is_klav_x_1 = False


def is_klav(board):
    if hero.is_klav_y_1:
        hero.count_y_1 += 1
        x, y = board.get_cell(hero.rect.x + hero.image.get_width() // 2,
                              hero.rect.y + hero.image.get_height() // 2 - hero.vy)
        if BOARD[y][x] == '_':
            hero.rect.y -= hero.vy

    if hero.is_klav_y_2:
        hero.count_y_2 += 1
        x, y = board.get_cell(hero.rect.x + hero.image.get_width() // 2,
                              hero.rect.y + hero.image.get_height() // 2 + hero.vy)
        if BOARD[y][x] == '_':
            hero.rect.y += hero.vy

    if hero.is_klav_x_0:
        hero.count_x_0 += 1
        x, y = board.get_cell(hero.rect.x + hero.image.get_width() // 2 + hero.vx,
                              hero.rect.y + hero.image.get_height() // 2)
        if BOARD[y][x] == '_':
            hero.rect.x += hero.vx
    if hero.is_klav_x_1:
        hero.count_x_1 += 1
        x, y = board.get_cell(hero.rect.x + hero.image.get_width() // 2 - hero.vx,
                              hero.rect.y + hero.image.get_height() // 2)
        if BOARD[y][x] == '_':
            hero.rect.x -= hero.vx
    if hero.is_atack:
        hero.count_atack += 1


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()

    board = Board()
    # for i in range(20):
    #     spider = Spider(750, 300, 3, 50, board, vision=30)
    #     spider_group.add(spider)
    # for i in range(30):
    #     spider = Spider(WIDTH // 2 + 750, 300, 3, 80, board, vision=50)
    #     spider_group.add(spider)
    # for i in range(40):
    #     spider = Spider(WIDTH // 2 + 750, HEIGTH // 2 + 300, 4, 100, board, vision=80)
    #     spider_group.add(spider)
    # for i in range(50):
    #     spider = Spider(750, HEIGTH // 2 + 300, 5, 100, board, vision=100)
    #     spider_group.add(spider)

    full_screen = pygame.Surface(WINDOW_SIZE)
    board.render(full_screen)
    screen_mini = pygame.transform.scale(full_screen.copy(), (WIDTH // SCALE, HEIGTH // SCALE))
    screen_mini.set_alpha(ALPHA)
    screen_mini_temp = screen_mini.copy()
    screen_mini_temp.set_alpha(ALPHA)
    screen_bottom_panel = screen.copy()
    full_screen_temp = full_screen.copy()

    board.set_view(0, 0)
    runnig = True
    while runnig:
        is_klav(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
            if event.type == Timer_Spider_TYPE:
                pass
            handling_mouse_actions(event)
            handling_keyboard_actions(event)

        screen.fill((0, 0, 0))
        full_screen.blit(full_screen_temp, (0, 0))
        if hero.rect.x < WIDTH // 2 and hero.rect.y < HEIGTH // 2:
            all_sprites.update()
            all_sprites.draw(full_screen)
            screen.blit(full_screen, (0, 0), (0, 0, WIDTH // 2, HEIGTH // 2))
            all_sprites_mini.update()
            screen_mini.blit(screen_mini_temp, (0, 0))
            all_sprites_mini.draw(screen_mini)
            BottomPanel(screen, screen_mini)
            hero.level = 1
        elif hero.rect.x > WIDTH // 2 and hero.rect.y < HEIGTH // 2:
            all_sprites.update()
            all_sprites.draw(full_screen)
            screen.blit(full_screen, (0, 0), (WIDTH // 2, 0, WIDTH - WIDTH // 2, HEIGTH))
            all_sprites_mini.update()
            screen_mini.blit(screen_mini_temp, (0, 0))
            all_sprites_mini.draw(screen_mini)
            BottomPanel(screen, screen_mini)
            hero.level = 2
        elif hero.rect.x > WIDTH // 2 and hero.rect.y > HEIGTH // 2:
            all_sprites.update()
            all_sprites.draw(full_screen)
            screen.blit(full_screen, (0, 0), (WIDTH // 2, HEIGTH // 2, WIDTH - WIDTH // 2, HEIGTH))
            all_sprites_mini.update()
            screen_mini.blit(screen_mini_temp, (0, 0))
            all_sprites_mini.draw(screen_mini)
            BottomPanel(screen, screen_mini)
            hero.level = 3
        elif hero.rect.x < WIDTH // 2 and hero.rect.y > HEIGTH // 2:
            all_sprites.update()
            all_sprites.draw(full_screen)
            screen.blit(full_screen, (0, 0), (0, HEIGTH // 2, WIDTH - WIDTH // 2, HEIGTH))
            all_sprites_mini.update()
            screen_mini.blit(screen_mini_temp, (0, 0))
            all_sprites_mini.draw(screen_mini)
            BottomPanel(screen, screen_mini)
            hero.level = 4
        screen.blit(screen_mini, (5, pygame.display.Info().current_h - screen_mini.get_height() - 5))
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


mini_hero = MiniHero()
hero = Hero(50, 300)
hero_group.add(hero)

if __name__ == '__main__':
    main()
