import os
import sys

import pygame
import pytmx

WINDOW_SIZE = WIDTH, HEIGTH = 1370, 800
fps = 30

all_sprites = pygame.sprite.Group()
spider_group = pygame.sprite.Group()


def load_image(name, anime):
    full_name = f'data/image/{anime}/{name}'
    if not os.path.isfile(full_name):
        print(full_name)
        print('lklkj')
        sys.exit()
    image = pygame.image.load(full_name)

    return image


class Spider(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)


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
        self.live = 50

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

        pygame.draw.rect(self.image, (0, 255, 0), (5, 0, int((20 / 100) * self.live), 5))
        pygame.draw.rect(self.image, (0, 255, 0), (5, 0, 20, 5), 1)


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


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    board = Board()
    hero = Hero(12, 2)
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
