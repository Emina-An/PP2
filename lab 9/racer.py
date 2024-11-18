import pygame
import sys
import random
import time

pygame.init()  # Инициализация pygame

# Установите частоту кадров
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Параметры экрана и игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Начальная скорость врага
COIN_SPAWN_RATE = 1000  # Частота появления монет в миллисекундах
COLLECTED_COINS = 0
COIN_WEIGHT_VALUES = [1, 3, 5]  # Возможные значения веса монет
COINS_FOR_SPEED_UP = 10  # Количество монет для увеличения скорости

# Экран отображения
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Шрифт для текста
font = pygame.font.Font(None, 36)

# Определение класса врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy1.png")  # Загрузка изображения врага
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)    

    def move(self):
        self.rect.move_ip(0, SPEED)  # Движение врага вниз по экрану
        if self.rect.top > SCREEN_HEIGHT:
            # Возвращаем врага наверх, если он выходит за нижнюю границу экрана
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)

# Определение класса игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player1.png")  # Загрузка изображения игрока
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция игрока

    def move(self):
        # Управление с помощью стрелок
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

# Определение класса монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin1.png")  # Загрузка изображения монеты
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), random.randint(0, SCREEN_HEIGHT // 2))
        self.speed = 4
        # Выбираем случайный вес монеты
        self.weight = random.choice(COIN_WEIGHT_VALUES)

    def move(self):
        self.rect.move_ip(0, self.speed)  # Движение монеты вниз
        if self.rect.top > SCREEN_HEIGHT:
            # Возвращаем монету наверх, если она выходит за нижнюю границу экрана
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)


# Создаем объекты
P1 = Player()
E1 = Enemy()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Таймеры для событий
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, COIN_SPAWN_RATE)

# Задержка перед началом игры
time.sleep(2)  # Задержка перед началом игры

# Главный цикл игры
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            # Увеличиваем скорость врага каждую секунду
            SPEED += 2
        if event.type == SPAWN_COIN:
            # Спавн монеты по таймеру
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == pygame.QUIT:
            # Завершаем игру при выходе
            pygame.quit()
            sys.exit()

    # Заполняем экран белым цветом
    DISPLAYSURF.fill(WHITE)

    # Отображаем и перемещаем все спрайты
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверяем столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()  # Удаляем все спрайты
        time.sleep(2)
        pygame.quit()
        sys.exit()        

    # Проверяем столкновение с монетами и учитываем их вес
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collected_coins:
        COLLECTED_COINS += coin.weight  # Увеличиваем счётчик на вес монеты

    # Увеличиваем скорость врага, если собрано N монет
    if COLLECTED_COINS >= COINS_FOR_SPEED_UP:
        SPEED += 1
        COINS_FOR_SPEED_UP += 10  # Увеличиваем порог для следующего увеличения скорости

    # Отображаем счётчик монет на экране
    coin_text = font.render("Coins: " + str(COLLECTED_COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 120, 10))

    pygame.display.update()
    FramePerSec.tick(FPS)
