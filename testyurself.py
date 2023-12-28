import pygame
import os
import sys


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
    return new_player, x, y, len(level[0]) * 50


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    #подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, ' '), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, obstacles_sprites)
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, player_sprite)
        self.image = load_image('pomedor.png')
        self.image = pygame.transform.scale(self.image, (45, 45))
        self.rect = self.image.get_rect().move(x, y)
        self.jumpfly = False
        self.start_y = y
        self.width = self.image.get_width()
        self.height = self. image.get_height()
        self.jump = 0
        self.fixed = False
        self.count = 0


    def update(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            dx += -10

        elif keys[pygame.K_RIGHT]:
            dx += 10

        if keys[pygame.K_SPACE]:
            self.jump = -20

        self.jump += 3
        if self.jump > 20:
            self.jump = 20
        dy += self.jump

        for sprite in all_sprites:
            if sprite not in player_sprite:
                if sprite.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # камера с левого и правого угла
                    dx = 0
                if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.jump < 0:
                        dy = sprite.rect.bottom - self.rect.top
                        self.jump = 0
                    elif self.jump >= 0:
                        dy = sprite.rect.top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy
        if self.rect.x == 700:
            self.fixed = True

        if self.fixed:
            camera.dx = dx


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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1400, 800
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group() # все спрайты
    player_sprite = pygame.sprite.Group() # игрок
    platform_sprites = pygame.sprite.Group()  # поверхности
    obstacles_sprites = pygame.sprite.Group()  # препятствия
    enemy_sprites = pygame.sprite.Group()  # враги

    fon_1 = load_image('fon-1.png')
    fon_2 = load_image('fon-2.png')
    background_animation = 0
    background_animation_pole = 0

    player, level_x, level_y, weight_map = generate_level(load_level('map.txt'))

    camera = Camera()
    clock = pygame.time.Clock()
    FPS = 240

    running = True
    while running:
        x_fon = player.rect.x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        x_fon_after = player.rect.x
        anim_bg = x_fon - x_fon_after

        # установка заднего фона
        screen.blit(fon_1, (background_animation_pole, 0))
        screen.blit(fon_1, (background_animation_pole + 1400, 0))
        screen.blit(fon_2, (background_animation, 0))
        screen.blit(fon_2, (background_animation + 1400, 0))
        background_animation -= 1
        background_animation_pole += anim_bg // 5
        if background_animation == -1400:
            background_animation = 0
        if background_animation_pole == -1400:
            background_animation_pole = 0

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        all_sprites.draw(screen)

        camera.dx = 0
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()