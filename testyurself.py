import pygame
import os
import sys


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    #подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    return image


class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, obstacles_sprites)



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


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # установка заднего фона
        screen.blit(fon_1, (0, 0))
        screen.blit(fon_2, (background_animation, 0))
        screen.blit(fon_2, (background_animation + 1400, 0))
        background_animation -= 1
        if background_animation == -1400:
            background_animation = 0

        pygame.display.flip()
    pygame.display.quit()