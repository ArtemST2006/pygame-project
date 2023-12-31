import pygame
import os
import sys
import random

pygame.init()
size = width, height = 1400, 750
screen = pygame.display.set_mode(size)


def check_hero(lis):
    for i in range(len(lis)):
        if '@' in lis[i]:
            return i
    return None


def generate_level(level):
    level.reverse()
    hero_y = len(level) - check_hero(level)
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                new_player = Player(x * 50, 750 - (y * 50))
            elif level[y][x] == '#':
                Platform(x * 50, 750 - (y * 50))
            elif level[y][x] == '*':
                Obstacles('ship', x * 50, 750 - (y * 50))
            elif level[y][x] == '!':
                Enemy(x * 50, 750 - (y * 50))
    return new_player, x, y, len(max(level, key=len))


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    # подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    return level_map


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def create_particles(position):
    particle_count = 20
    numbers = range(-10, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image('star.png')]
    for scale in (10, 25, 35):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(death, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect((0, 0, 1400, 800)):
            self.kill()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__(all_sprites, obstacles_sprites)
        self.image = load_image(OBSTACLES[name])
        if name == 'ship':
            self.image = pygame.transform.scale(self.image, (50, 40))
            self.rect = self.image.get_rect().move(x, y + 20)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, player_sprite)
        self.stop = pygame.transform.scale(load_image('stop_player.png'), (50, 46))
        self.image = self.stop
        self.rect = self.image.get_rect().move(x, y)
        self.jumpfly = False
        self.start_y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.jump = 0
        self.count = 0
        self.count_jump = 0
        self.camera_fixed = False
        self.left = False
        self.left = False

    def update(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx += -10
            self.count += 1
            self.image = A_PLAYER_L[self.count % len(A_PLAYER_L)]
            self.left = True
        elif keys[pygame.K_RIGHT]:
            dx += 10
            self.count += 1
            self.image = A_PLAYER_R[self.count % len(A_PLAYER_R)]
            self.left = False
        else:
            if self.left:
                self.image = self.stop
            else:
                self.image = pygame.transform.flip(self.stop, True, False)

        self.jump += 3
        if self.jump > 20:
            self.jump = 20
        dy += self.jump

        for sprite in platform_sprites:
            if sprite not in player_sprite:
                if sprite.rect.colliderect(self.rect.x + dx, self.rect.y, self.width,
                                           self.height):  # камера с левого и правого угла
                    dx = 0
                if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.jump < 0:
                        dy = sprite.rect.bottom - self.rect.top
                        self.jump = 0
                    elif self.jump >= 0:
                        self.count_jump = 0
                        dy = sprite.rect.top - self.rect.bottom
                        self.jumpfly = False

        self.rect.x += dx
        self.rect.y += dy

        self.camera(dx)

    def camera(self, dx):
        global left_border, right_border
        left_border += dx
        right_border -= dx

        if left_border <= 700 or right_border <= 700:
            self.camera_fixed = False
        else:
            self.camera_fixed = True

        if self.camera_fixed:
            camera.dx = dx


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(enemy_sprites, all_sprites)
        self.count = 0
        self.left = False
        self.make_image()
        self.rect = self.image.get_rect().move(x, y - 20)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0

    def make_image(self):
        self.count += 1
        if self.left:
            self.image = ZOMBIE_L[self.count % len(ZOMBIE_L)]
        else:
            self.image = ZOMBIE_R[self.count % len(ZOMBIE_R)]

    def update(self):
        dy = 8
        x_hero = player.rect.x
        x_zombie = self.rect.x

        if not player.jumpfly:
            if abs(x_hero - x_zombie) < 500:
                self.dx = 6
            else:
                self.dx = 0

            if x_hero < x_zombie:
                self.dx = -self.dx
                self.left = True
            else:
                self.left = False
        else:
            self.dx = self.dx

        for sprite in platform_sprites:
            if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                dy = sprite.rect.top - self.rect.bottom
            if sprite.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                pass
        if pygame.sprite.spritecollideany(self, obstacles_sprites):
            self.kill()
            create_particles((self.rect.x, self.rect.y))

        if self.dx != 0:
            self.make_image()

        self.rect.y += dy
        self.rect.x += self.dx


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(platform_sprites, all_sprites)
        self.image = load_image('zelma.png')
        self.rect = self.image.get_rect().move(x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy

    def update(self, target):
        self.dy = (target.rect.y - 450)


def cut_sheet(sheet, columns, rows):
    lis = []
    lis2 = []
    img = load_image(sheet)
    width_img = img.get_width() // columns
    height_img = img.get_height() // rows
    for j in range(rows):
        for i in range(columns):
            frame_location = i * width_img, j * height_img
            size = width_img, height_img
            img_new = img.subsurface(pygame.Rect(frame_location, size))
            img_new = pygame.transform.scale(img_new, (50, 50))
            img_new = img_new.subsurface(pygame.Rect((0, 0), (50, 46)))
            lis.append(img_new)
            lis2.append(pygame.transform.flip(img_new, True, False))
    return lis, lis2


def make_zombie():
    lis = []
    lis2 = []
    for i in range(1, 8):
        img = load_image(f'antiHero/anti_hero{i}.png')
        img = pygame.transform.scale(img, (46, 50))
        lis.append(img)
        lis2.append(pygame.transform.flip(img, True, False))
    return lis, lis2


if __name__ == '__main__':
    OBSTACLES = {'ship': 'ship.png'}
    GRAVITY = 1
    A_PLAYER_R, A_PLAYER_L = cut_sheet('player.png', 5, 2)
    ZOMBIE_R, ZOMBIE_L = make_zombie()

    all_sprites = pygame.sprite.Group()  # все спрайты
    player_sprite = pygame.sprite.Group()  # игрок
    platform_sprites = pygame.sprite.Group()  # поверхности
    obstacles_sprites = pygame.sprite.Group()  # препятствия
    enemy_sprites = pygame.sprite.Group()  # враги
    death = pygame.sprite.Group()  # star

    fon_1 = load_image('fon-1.png')
    fon_2 = load_image('fon-2.png')
    background_animation = 0
    background_animation_pole_x = 0
    background_animation_pole_y = 0

    player, level_x, level_y, weight_map, = generate_level(load_level('map.txt'))
    left_border = player.rect.x
    right_border = weight_map * 50 - player.rect.x - 50

    camera = Camera()
    clock = pygame.time.Clock()
    FPS = 30

    game = True
    running = True
    while running:
        # установка флага
        if (pygame.sprite.spritecollideany(player, obstacles_sprites) or pygame.sprite.spritecollideany(player,
                                                                                                        enemy_sprites)) and game:
            player.kill()
            game = False
            create_particles((player.rect.x, player.rect.y))
            count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.count_jump < 2:
                    player.jumpfly = True
                    player.count_jump += 1
                    player.jump = -20
        x_fon = player.rect.x
        all_sprites.update()

        # установка заднего фона
        x_fon_after = player.rect.x
        anim_bg_x = x_fon - x_fon_after

        if camera.dy < 0:  # vniz
            if not background_animation_pole_y + 1 >= 10:
                background_animation_pole_y += 1
        if camera.dy > 0:  # vverh
            if not background_animation_pole_y - 1 <= -10:
                background_animation_pole_y -= 1

        screen.blit(fon_1, (background_animation_pole_x, background_animation_pole_y))
        screen.blit(fon_1, (background_animation_pole_x + 1400, background_animation_pole_y))
        screen.blit(fon_2, (background_animation, 0))
        screen.blit(fon_2, (background_animation + 1400, 0))
        background_animation -= 1
        background_animation_pole_x += anim_bg_x // 10
        if background_animation == -1400:
            background_animation = 0
        if background_animation_pole_x == -1400:
            background_animation_pole = 0

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)
        camera.dx = 0
        if not game:
            count += 1
            if count > 50:  # меню
                print('end')
                pass

        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()
