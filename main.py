import os
import sys
from random import choice, randint

import pygame
import pytmx

pygame.init()
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


class Camera:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, pygame.display.Info().current_w, pygame.display.Info().current_h)

    def move(self, vector):
        self.rect[0] += vector[0]
        self.rect[1] += vector[1]


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, width, heigth):
        super(Border, self).__init__(all_sprites)
        self.image = pygame.Surface((width, heigth))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, width, heigth), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spider(pygame.sprite.Sprite):
    def __init__(self, x, y, v, live, vision=20):
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
        self.image = self.image_list_0[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y
        self.count = 0
        self.direction = 0
        self.list_direction = [0, 1, 2, 3]

    def update(self):
        if self.hp <= 0:
            self.image = self.image_h_list[self.count % 4]
            self.vy = 0
            self.vx = 0

            if self.count > 28:
                spider_group.remove(self)
                self.kill()

        elif pygame.sprite.spritecollideany(self, vertical_borders):

            self.vx *= -1
            self.vy *= -1
        elif pygame.sprite.spritecollideany(self, horizontal_borders):

            self.vy *= -1
            self.vx *= -1
        else:

            if self.direction == 0:
                self.image = self.image_list_0[self.count % 6]
                self.vy = -self.v
                self.vx = 0
            if self.direction == 1:
                self.image = self.image_list_1[self.count % 6]
                self.vy = self.v
                self.vx = 0
            if self.direction == 2:
                self.vy = 0
                self.vx = -self.v
                self.image = self.image_list_2[self.count % 6]
            if self.direction == 3:
                self.vy = 0
                self.vx = self.v
                self.image = self.image_list_3[self.count % 6]
        self.count += 1
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, hero_group) and hero.is_atack:
            self.hp -= hero.damage
        pygame.draw.rect(self.image, (0, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 0)
        pygame.draw.rect(self.image, (255, 0, 0),
                         (self.image.get_width() // 2 - 10, 0, int((20 / self.live_max) * self.hp), 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 1)
        self.object_protection()
        self.metod_vision()
        self.metod_atack()

    def object_protection(self):
        if self.count % 30 == 0:
            a = self.list_direction.pop(self.list_direction.index(self.direction))
            self.direction = choice(self.list_direction)
            self.list_direction.append(a)
            self.count = 0

    def metod_vision(self):
        x_1, y_1, r_1 = self.rect.x, self.rect.y, self.vision
        x_2, y_2, r_2 = hero.rect.x, hero.rect.y, hero.rect.width
        l = ((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2) ** 0.5

        if l <= r_1 + r_2:
            self.is_atack = True
        else:
            self.is_atack = False

    def metod_atack(self):
        if self.is_atack:
            INF = 1000
            # x, y = board.get_cord(self.rect.x, self.rect.y)
            # print(x, y)
            # dictance = [[INF] * 100 for i in range(100)]
            # dictance[x][y] = 0


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
        # for obj in object_sprites:
        #     if pygame.sprite.collide_mask(self, obj):
        #         if self.is_klav_x_0:
        #             self.rect.x -= 20
        #         if self.is_klav_x_1:
        #             self.rect.x += 20
        #         if self.is_klav_y_1:
        #             self.rect.y += 20
        #         if self.is_klav_y_2:
        #             self.rect.y -= 20

        # self.rect = self.rect.move(self.vx, self.vy)
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
        screen.set_alpha(200)
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


class Object_Map(pygame.sprite.Sprite):
    def __init__(self, image, y, x, cell_size):
        super().__init__(object_sprites)
        self.rect = image.get_rect()
        self.rect.x = x * cell_size
        self.rect.y = y * cell_size
        self.mask = pygame.mask.from_surface(image)


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

                    if self.map.get_tile_gid(x, y, 1) not in [122, 123, 135, 136, 182, 183, 199, 200]:
                        object_sprites.add(Object_Map(image_1, y, x, self.cell_size))
                        id_tiled = self.map.get_tile_gid(x, y, 1)
                        BOARD[y][x] = id_tiled
                    screen_1.blit(image_1, (self.left + x * self.cell_size, self.top + y * self.cell_size))

        for row in BOARD:
            print(row)
        return screen_1

    def get_cell(self, x, y):
        return x // self.cell_size, y // self.cell_size


def border():
    horizontal_borders.add(Border(0, 0, WIDTH, 1))
    horizontal_borders.add(Border(0, HEIGTH - 1, WIDTH, 1))
    vertical_borders.add(Border(0, 0, 1, HEIGTH))
    vertical_borders.add(Border(WIDTH - 1, 0, 1, HEIGTH))


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
    border()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode()

    board = Board()

    screen_1 = pygame.Surface(WINDOW_SIZE)
    screen_1 = board.render(screen_1).copy()
    screen_mini = pygame.transform.scale(screen_1.copy(), (WIDTH // SCALE, HEIGTH // SCALE))
    screen_mini.set_alpha(ALPHA)
    screen_mini_1 = screen_mini.copy()
    screen_mini_1.set_alpha(ALPHA)
    screen_bottom_panel = screen_1.copy()

    for i in range(10):
        spider = Spider(randint(10, 1000), randint(10, 500), min((i + 1) * 5, 3), min((i + 1) * 50, 200))
        spider_group.add(spider)

    board.set_view(0, 0)
    runnig = True
    while runnig:
        is_klav(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
            handling_mouse_actions(event)
            handling_keyboard_actions(event)

        BottomPanel(screen_bottom_panel, screen_mini)
        screen.fill((0, 0, 0))

        all_sprites.update()
        screen.blit(screen_bottom_panel, (0, 0))
        all_sprites.draw(screen)

        all_sprites_mini.update()
        screen_mini.blit(screen_mini_1, (0, 0))
        all_sprites_mini.draw(screen_mini)

        screen.blit(screen_mini, (5, pygame.display.Info().current_h - screen_mini.get_height() - 5))
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


mini_hero = MiniHero()
hero = Hero(pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)
hero_group.add(hero)
camera = Camera(50, 50)

if __name__ == '__main__':
    main()
