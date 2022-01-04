import os
import sys
from random import choice, randint

import pygame
import pytmx

WINDOW_SIZE = WIDTH, HEIGTH = 1370, 800
fps = 30

all_sprites = pygame.sprite.Group()
spider_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()


def load_image(name, anime):
    full_name = f'data/image/{anime}/{name}'
    if not os.path.isfile(full_name):
        print(full_name)
        print('lklkj')
        sys.exit()
    image = pygame.image.load(full_name)

    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y, width, heigth):
        super(Border, self).__init__(all_sprites)
        self.image = pygame.Surface((width, heigth))
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, width, heigth), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spider(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.vx = 0
        self.vy = 0
        self.position()
        self.x = x
        self.y = y
        self.live = 50
        self.is_atack = False

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
        self.rect = self.image.get_rect()

        self.rect.x = 500
        self.rect.y = 400
        self.count = 0
        self.direction = 0
        self.list_direction = [0, 1, 2, 3]

    def update(self):
        if self.live <= 0:
            self.image = self.image_h_list[self.count % 4]
            self.vy = 0
            self.vx = 0

            if self.count > 28:
                spider_group.remove(self)
                self.kill()

        elif pygame.sprite.spritecollideany(self, vertical_borders):
            print(self)
            self.vx *= -1
            self.vy *= -1
        elif pygame.sprite.spritecollideany(self, horizontal_borders):
            print(self)
            self.vy *= -1
            self.vx *= -1
        else:

            if self.direction == 0:
                self.image = self.image_list_0[self.count % 6]
                self.vy = -5
                self.vx = 0
            if self.direction == 1:
                self.image = self.image_list_1[self.count % 6]
                self.vy = 5
                self.vx = 0
            if self.direction == 2:
                self.vy = 0
                self.vx = -5
                self.image = self.image_list_2[self.count % 6]
            if self.direction == 3:
                self.vy = 0
                self.vx = 5
                self.image = self.image_list_3[self.count % 6]
        self.count += 1
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, hero_group) and hero.is_atack:
            self.live -= 10
        pygame.draw.rect(self.image, (0, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 0)
        pygame.draw.rect(self.image, (255, 0, 0), (self.image.get_width() // 2 - 10, 0, int((20 / 100) * self.live), 5))
        pygame.draw.rect(self.image, (255, 0, 0), (self.image.get_width() // 2 - 10, 0, 20, 5), 1)
        self.object_protection()

    def object_protection(self):
        if self.count % 30 == 0:
            a = self.list_direction.pop(self.list_direction.index(self.direction))
            self.direction = choice(self.list_direction)
            self.list_direction.append(a)
            self.count = 0


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)

        self.vx = 0
        self.vy = 0
        self.move()
        self.atack()

    def atack(self):
        self.image_atack_lict = [load_image('hero_a_0.png', 'hero'), load_image('hero_a_1.png', 'hero'),
                                 load_image('hero_a_2.png', 'hero'),
                                 load_image('hero_a_3.png', 'hero'),
                                 load_image('hero_a_4.png', 'hero')]
        self.is_atack = False
        self.count_atack = 0
        self.live = 1000

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
        self.rect.x, self.rect.y = 50, 50

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

        self.rect = self.rect.move(self.vx, self.vy)
        list_atack = pygame.sprite.spritecollide(self, spider_group, False)
        if list_atack:
            for spider in list_atack:
                if spider.live > 0:
                    self.live = max(self.live - 1, 0)

        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, 20, 5), 0)
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, (20 * self.live) // 100, 5))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, 20, 5), 1)
        self.mask = pygame.mask.from_surface(self.image)


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
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)

                if image:
                    screen.blit(image, (self.left + x * self.cell_size, self.top + y * self.cell_size))
                image_1 = self.map.get_tile_image(x, y, 1)
                if image_1:
                    screen.blit(image_1, (self.left + x * self.cell_size, self.top + y * self.cell_size))

    def get_cord(self, x, y):
        return self.left + self.cell_size * x, self.top + self.cell_size * y


hero = Hero(12, 2)
hero_group.add(hero)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    horizontal_borders.add(Border(0, 0, WIDTH, 10))
    horizontal_borders.add(Border(0, HEIGTH - 10, WIDTH, 10))
    vertical_borders.add(Border(0, 0, 10, HEIGTH))
    vertical_borders.add(Border(WIDTH - 10, 0, 10, HEIGTH))

    board = Board()

    for i in range(10):
        spider = Spider(randint(10, 1000), randint(10, 500))
        spider_group.add(spider)

    board.set_view(0, 0)
    runnig = True
    while runnig:
        if hero.is_klav_y_1:
            hero.count_y_1 += 1
        if hero.is_klav_y_2:
            hero.count_y_2 += 1
        if hero.is_klav_x_0:
            hero.count_x_0 += 1
        if hero.is_klav_x_1:
            hero.count_x_1 += 1
        if hero.is_atack:
            hero.count_atack += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runnig = False
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    sys.exit()
                if event.key == pygame.K_w:
                    hero.is_klav_y_1 = True
                    hero.vy = -10

                if event.key == pygame.K_s:
                    hero.is_klav_y_2 = True
                    hero.vy = 10
                if event.key == pygame.K_d:
                    hero.vx = 10
                    hero.is_klav_x_0 = True
                if event.key == pygame.K_a:
                    hero.vx = -10
                    hero.is_klav_x_1 = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.is_klav_y_1 = False
                    hero.count_y_1 = 0
                    hero.vy = 0
                if event.key == pygame.K_s:
                    hero.is_klav_y_2 = False
                    hero.count_y_2 = 0
                    hero.vy = 0
                if event.key == pygame.K_d:
                    hero.vx = 0
                    hero.count_x_0 = 0
                    hero.is_klav_x_0 = False
                if event.key == pygame.K_a:
                    hero.vx = 0
                    hero.count_x_1 = 0
                    hero.is_klav_x_1 = False

        screen.fill((0, 0, 0))
        board.render(screen)

        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
