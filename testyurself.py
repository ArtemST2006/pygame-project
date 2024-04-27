import pygame
import os
import sys
import random

pygame.mixer.pre_init(44100, -16, 1, 512)  # для воспроизведения без задержки
pygame.init()
size = width, height = 1400, 750
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 30


def terminate():
    pygame.quit()
    sys.exit()


def get_level():
    return os.listdir('data/LEVELS')


def start_screen():
    intro_text = ["PLACEHOLDER",
                  "Нажмите любую кнопку"]

    fon_1 = load_image('fon-1.png')
    fon_2 = load_image('fon-2.png')
    screen.blit(fon_1, (0, 0))
    screen.blit(fon_2, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 700 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    intro_text = ["PLACEHOLDER",
                  "Вы прошли все уровни игры (на данный момент).", "Поздравляем!"]

    fon_1 = load_image('fon-1.png')
    fon_2 = load_image('fon-2.png')
    screen.blit(fon_1, (0, 0))
    screen.blit(fon_2, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 700 - intro_rect.width // 2
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def check_hero(lis):
    for i in range(len(lis)):
        if '@' in lis[i]:
            return i
    return None


def generate_level(level):
    #  создаём карту
    level.reverse()
    new_player, x, y = None, None, None
    try:
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '@':
                    new_player = Player(x * 50, 750 - (y * 50))

                elif level[y][x] == '#':
                    try:
                        if level[y + 1][x] != '#' or level[y + 1][x] == '*':
                            Platform(x * 50, 750 - (y * 50), 'trava')
                        else:
                            Platform(x * 50, 750 - (y * 50), 'zelma')
                    except Exception:
                        Platform(x * 50, 750 - (y * 50), 'zelma')

                elif level[y][x] == '*':
                    Obstacles('ship', x * 50, 750 - (y * 50))

                elif level[y][x] == '!':
                    EnemyZombie(x * 50, 750 - (y * 50))

                elif level[y][x] == '0':
                    EnemyBublic(x * 50, 750 - (y * 50))

                elif level[y][x] == '+':
                    Win(x * 50, 750 - (y * 50))

                elif level[y][x] == '5':
                    Gain(x * 50, 750 - (y * 50), level[y][x])

                elif level[y][x] == '1':
                    Star(x * 50, 750 - (y * 50), level[y][x])

                elif level[y][x] == '&':
                    try:
                        if level[y][x - 1] == '#':
                            EnemyPush(x * 50, 750 - (y * 50), 'right')
                        else:
                            EnemyPush(x * 50, 750 - (y * 50), 'left')
                    except Exception:
                        pass

                elif level[y][x] == '^':
                    try:
                        if level[y + 1][x] == '#':
                            EnemyPush(x * 50, 750 - (y * 50), 'botton')
                        else:
                            EnemyPush(x * 50, 750 - (y * 50), 'top')
                    except Exception:
                        pass

                elif level[y][x] == '%':
                    CircularSaw(x * 50, 750 - (y * 50))
    except Exception:
        pass


    return new_player, x, y, len(max(level, key=len))


def load_level(filename):
    filename = "data/LEVELS/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line for line in mapFile]
    # подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    return level_map


def load_image(name, colorkey=None):
    #  присваиваем картинки
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


def load_sound_little(name):
    #  звуки действий
    try:
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print('error')
            sys.exit()

        return pygame.mixer.Sound(fullname)
    except Exception:
        return None


def load_music(name):
    #  музыкальное сопровождение
    try:
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print('error')
            sys.exit()

        pygame.mixer.music.load(fullname)
    except Exception:
        return


def play_music(k):
    #  определяем какой именно звук нужен
    if k == 1:
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    elif k == 2:
        pygame.mixer.music.pause()
    elif k == -2:
        pygame.mixer.music.unpause()
    elif k == 0:
        pygame.mixer.music.stop()


def create_particles(k, position):
    #  создаём звёзды для звёздочной системы
    particle_count = 20
    numbers = range(-10, 15)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), k)


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image('star.png')]
    maso = [pygame.transform.scale(load_image('maso.png'), (20, 20))]
    for scale in (10, 25, 35):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))
        maso.append(pygame.transform.scale(maso[0], (scale, scale)))

    def __init__(self, pos, dx, dy, k):
        super().__init__(death, all_sprites)
        if k == 'win':
            self.image = random.choice(self.fire)
        else:
            self.image = random.choice(self.maso)
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
    #  класс прептствий
    def __init__(self, name, x, y):
        super().__init__(all_sprites, obstacles_sprites)
        self.image = load_image(BLOCK[name])
        if name == 'ship':
            self.image = pygame.transform.scale(self.image, (50, 40))
            self.rect = self.image.get_rect().move(x, y + 20)


class Player(pygame.sprite.Sprite):
    #  класс игрока
    def __init__(self, x, y):
        super().__init__(player_sprite, all_sprites)
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
        self.is_gain = False
        self.count_gain = 0
        self.count_star = 0

    def update(self):
        global count
        if count == 0:
            dx = 0
            dy = 0

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx += -10
                self.count += 1
                self.image = A_PLAYER_L[self.count % len(A_PLAYER_L)]
                self.left = True
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += 10
                self.count += 1
                self.image = A_PLAYER_R[self.count % len(A_PLAYER_R)]
                self.left = False
            else:
                if self.left:
                    self.image = self.stop
                else:
                    self.image = pygame.transform.flip(self.stop, True, False)

            #  гравитация
            self.jump += 3
            if self.jump > 30:
                self.jump = 30
            dy += self.jump

            #  отслеживаем не сталкнётся ли игрок с землёй
            for sprite in platform_sprites:
                if sprite not in player_sprite:
                    if sprite.rect.colliderect(self.rect.x + dx, self.rect.y, self.width,
                                               self.height):
                        dx = 0
                    if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.jump < 0:
                            dy = sprite.rect.bottom - self.rect.top
                            self.jump = 0
                        elif self.jump >= 0:
                            self.count_jump = 0
                            dy = sprite.rect.top - self.rect.bottom
                            self.jumpfly = False

            #  отслеживаем столкновение с звёздочками уилениями и бубликом
            for sprite in gain_sprites:
                if sprite.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    sprite.kill()
                    self.is_gain = True
                    self.count_gain = 0

            for sprite in star_point:
                if sprite.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                    sprite.kill()
                    self.count_star += 1

            for sprite in bublic_sprites:
                if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    death_ship_sound.play()
                    sprite.kill()
                    self.jump = -10
                    create_particles('death', (sprite.rect.x, sprite.rect.y))
                    game = False

            if self.is_gain:
                self.count_gain += 1
            if self.count_gain > 200:
                self.is_gain = False
                self.count_gain = 0

            self.rect.x += dx
            self.rect.y += dy

            self.camera(dx)

    def camera(self, dx):
        #  определяем, нужно ли движение камеры
        global left_border, right_border
        left_border += dx
        right_border -= dx

        if left_border <= 700 or right_border <= 700:
            self.camera_fixed = False
        else:
            self.camera_fixed = True

        if self.camera_fixed:
            camera.dx = dx


class EnemyZombie(pygame.sprite.Sprite):
    #  класс зомбиков
    def __init__(self, x, y):
        super().__init__(enemy_sprites, all_sprites, zombie_sprites)
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
                self.dx = 0
        if pygame.sprite.spritecollideany(self, obstacles_sprites):
            self.kill()
            death_ship_sound.play()
            create_particles('death', (self.rect.x, self.rect.y))

        if abs(x_hero - x_zombie) < 500:
            self.make_image()

        self.rect.y += dy
        self.rect.x += self.dx


class EnemyBublic(pygame.sprite.Sprite):
    #  кдасс бублика
    def __init__(self, x, y):
        super().__init__(all_sprites, enemy_sprites, bublic_sprites)
        self.image = pygame.transform.scale(load_image(BLOCK['bublic']), (50, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.left = False

    def update(self):
        dx = 11

        if self.left:
            dx = -10

        for sprite in platform_sprites:
            if sprite.rect.colliderect(self.rect.x + dx, self.rect.y, self.width,
                                        self.height):  # камера с левого и правого угла
                dx = 0
                self.left = not self.left

        self.rect.x += dx


class EnemyPush(pygame.sprite.Sprite):
    #   класс пушки
    def __init__(self, x, y, name):
        super().__init__(enemy_sprites, all_sprites)
        self.dx = 0
        self.dy = 0

        if name == 'left':
            self.image = load_image(BLOCK['push'])
            self.dx = - 10
        elif name == 'right':
            self.dx = 10
            self.image = pygame.transform.flip(load_image(BLOCK['push']), True, False)
        elif name == 'top':
            self.image = load_image(BLOCK['push'])
            self.dy = -10
        else:
            self.image = load_image(BLOCK['push'])
            self.dy = 10

        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.count = 0
        self.x, self.y = x, y

    def update(self):
        self.count += 1
        if self.count % 40 == 0:
            self.make_pul()

    def make_pul(self):
        Pulka(self.rect.x, self.rect.y, self.dx, self.dy)


class Pulka(pygame.sprite.Sprite):
    #  отдельный класс пульки
    def __init__(self, x, y, dx, dy):
        super().__init__(enemy_sprites, pulki)
        self.dx = dx
        self.dy = dy
        self.image = load_image(BLOCK['pulka'])
        self.image = pygame.transform.scale(self.image, (20, 15))
        self.rect = self.image.get_rect().move(x + 25, y + 25)
        self.count = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if pygame.sprite.spritecollideany(self, platform_sprites):
            self.kill()


class Platform(pygame.sprite.Sprite):
    #  поверхности
    def __init__(self, x, y, name):
        super().__init__(platform_sprites, all_sprites)
        self.image = load_image(BLOCK[name])
        self.rect = self.image.get_rect().move(x, y)


class Win(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(win_pos, all_sprites)
        self.image = load_image(BLOCK['flag'])
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect().move(x, y)


class CircularSaw(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, enemy_sprites)
        self.lis_image = [pygame.transform.scale(load_image('Circularca/1.png'), (50, 50)),
                          pygame.transform.scale(load_image('Circularca/2.png'), (50, 50)),
                          pygame.transform.scale(load_image('Circularca/3.png'), (50, 50)),
                          pygame.transform.scale(load_image('Circularca/4.png'), (50, 50)),
                          pygame.transform.scale(load_image('Circularca/5.png'), (50, 50))]
        self.image = self.lis_image[0]

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect().move(x, y)

        self.count = 0
        self.delay = 0
        self.flag = True

    def update(self):
        if self.flag:
            dy = -6
        else:
            dy = 6

        self.count += 1
        self.image = self.lis_image[self.count % 5]

        if self.delay == 0:
            for sprite in platform_sprites:
                if sprite.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.flag:
                        dy = sprite.rect.bottom - self.rect.top
                    else:
                        dy = sprite.rect.top - self.rect.bottom

                    self.flag = not self.flag

                    self.delay = -10
            self.rect.y += dy
        else:
            self.delay += 1



class Gain(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(all_sprites, gain_sprites)
        self.image = load_image(BLOCK[name])
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect().move(x + 10, y - 10)
        self.count = 0

        if name == '5':
            gain_big_jump.add(self)

    def update(self):
        self.count += 1
        if self.count % 4 == 0:
            self.rect.y += random.choice([1, -1])


class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__(all_sprites, star_point)
        self.image = load_image(BLOCK[name])
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect().move(x + 10, y)


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
    start_screen()
    load_music('sounds/all_music_fon.mp3')
    death_ship_sound = load_sound_little('sounds/death_of_ship.ogg')
    jump_sound = load_sound_little('sounds/prijoc.ogg')
    game_won = load_sound_little('sounds/game-won.ogg')
    play_music(1)

    LEVELS = get_level()
    BLOCK = {'ship': 'ship.png', 'trava': 'trava.png',
             'zelma': 'zelma.png', '5': 'gain/big_jump.png',
             '1': 'star.png', 'push': 'pusha/push.png',
             'flag': 'flag.png', 'bublic': 'bublic/bublic1.png',
             'pulka': 'pusha/pulka.png'}
    GRAVITY = 1
    A_PLAYER_R, A_PLAYER_L = cut_sheet('player.png', 5, 2)
    ZOMBIE_R, ZOMBIE_L = make_zombie()

    all_sprites = pygame.sprite.Group()  # все спрайты
    player_sprite = pygame.sprite.Group()  # игрок
    platform_sprites = pygame.sprite.Group()  # поверхности
    obstacles_sprites = pygame.sprite.Group()  # препятствия
    enemy_sprites = pygame.sprite.Group()  # враги
    zombie_sprites = pygame.sprite.Group()  # зомби
    bublic_sprites = pygame.sprite.Group()  # бублик враг
    puska_sprites = pygame.sprite.Group()  # пушка
    pulki = pygame.sprite.Group()
    death = pygame.sprite.Group()  # star
    win_pos = pygame.sprite.Group()
    star_point = pygame.sprite.Group()
    gain_sprites = pygame.sprite.Group()  # все усиления
    gain_big_jump = pygame.sprite.Group()

    fon_1 = load_image('fon-1.png')
    fon_2 = load_image('fon-2.png')
    background_animation = 0
    background_animation_pole_x = 0
    background_animation_pole_y = 0
    player, level_x, level_y, weight_map, = generate_level(load_level(LEVELS[0]))
    left_border = player.rect.x
    right_border = weight_map * 50 - player.rect.x - 50

    camera = Camera()

    current_level_index = 0
    game = True
    running = True
    count = 0
    while running:
        # установка флага
        if (pygame.sprite.spritecollideany(player, obstacles_sprites) or
                pygame.sprite.spritecollideany(player, enemy_sprites)) and game:  # смерть
            death_ship_sound.play()
            player.kill()
            game = False
            create_particles('death', (player.rect.x, player.rect.y))
            count = 0
        if pygame.sprite.spritecollideany(player, win_pos) and game:  # прохождение уровня
            current_level_index += 1
            game_won.play()
            player.kill()
            game = False
            create_particles('win', (player.rect.x, player.rect.y))
            count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.count_jump < 2:
                    jump_sound.play()
                    player.jumpfly = True
                    player.count_jump += 1
                    if player.is_gain:
                        player.jump = -30
                    else:
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

        #  движение заднего фона
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
        for sp in pulki:
            camera.apply(sp)
        pulki.update()
        pulki.draw(screen)
        all_sprites.draw(screen)
        camera.dx = 0
        if not game:  # если игрок умер или прошёл
            count += 1
            if count > 30:
                screen.fill((0, 0, 0))
                all_sprites = pygame.sprite.Group()
                player_sprite = pygame.sprite.Group()
                platform_sprites = pygame.sprite.Group()
                obstacles_sprites = pygame.sprite.Group()
                enemy_sprites = pygame.sprite.Group()
                zombie_sprites = pygame.sprite.Group()
                bublic_sprites = pygame.sprite.Group()
                puska_sprites = pygame.sprite.Group()
                pulki = pygame.sprite.Group()
                death = pygame.sprite.Group()
                win_pos = pygame.sprite.Group()
                star_point = pygame.sprite.Group()
                gain_sprites = pygame.sprite.Group()
                gain_big_jump = pygame.sprite.Group()
                try:
                    player, level_x, level_y, weight_map, = generate_level(load_level(LEVELS[current_level_index]))
                except IndexError:
                    end_screen()
                    break
                fon_1 = load_image('fon-1.png')
                fon_2 = load_image('fon-2.png')
                background_animation = 0
                background_animation_pole_x = 0
                background_animation_pole_y = 0
                left_border = player.rect.x
                right_border = weight_map * 50 - player.rect.x - 50

                count = 0
                game = True
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()
