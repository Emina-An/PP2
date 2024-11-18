import pygame
import random
import time
time.sleep(5)  # Задержка на 5 секунд перед выходом
 
# Настройки игры
snake_speed = 15
HEIGHT = 720
WIDTH = 480

# Цвета
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Инициализация pygame
pygame.init()
pygame.display.set_caption('Snake')
game_window = pygame.display.set_mode((HEIGHT, WIDTH))
fps = pygame.time.Clock()

# Параметры змейки
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
direction = 'RIGHT'
change_to = direction

# Очки и уровень
score = 0
level = 1

# Создание еды с разным весом и временем исчезновения
def generate_food():
    pos = [random.randrange(1, (HEIGHT // 10)) * 10,
           random.randrange(1, (WIDTH // 10)) * 10]
    weight = random.choice([5, 10, 15])  # Вес еды
    timer = random.randint(50, 150)  # Таймер для исчезновения еды
    return {"position": pos, "weight": weight, "timer": timer}

foods = [generate_food()]  # Начальная еда

# Функция отображения очков и уровня
def show_score_level():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render('Score: ' + str(score) + '  Level: ' + str(level), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (HEIGHT / 10, 15)
    game_window.blit(score_surface, score_rect)

# Функция завершения игры
def game_over():
    font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = font.render('Your Score: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (HEIGHT / 2, WIDTH / 4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    # Изменение направления
    direction = change_to

    # Движение змейки
    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10

    # Увеличение длины змейки
    snake_body.insert(0, list(snake_position))

    # Проверка на столкновение с едой
    food_eaten = False
    for food in foods[:]:
        if snake_position == food["position"]:
            score += food["weight"]
            foods.remove(food)
            food_eaten = True
            break

    # Удаление последнего сегмента, если еда не съедена
    if not food_eaten:
        snake_body.pop()

    # Создание новой еды, если текущей нет
    if len(foods) < 3:  # Поддерживаем не более 3 единиц еды
        foods.append(generate_food())

    # Проверка для перехода на новый уровень
    if score // 30 + 1 > level:
        level += 1
        snake_speed += 5

    # Очистка экрана
    game_window.fill(black)

    # Отображение змейки
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Отображение еды и уменьшение таймера
    for food in foods[:]:
        food["timer"] -= 1  # Уменьшение таймера для исчезновения еды
        if food["timer"] <= 0:
            foods.remove(food)  # Удаляем еду, если таймер истек
        else:
            pygame.draw.rect(game_window, white, pygame.Rect(food["position"][0], food["position"][1], 10, 10))

    # Проверка на столкновение с границей
    if snake_position[0] < 0 or snake_position[0] > HEIGHT - 10 or snake_position[1] < 0 or snake_position[1] > WIDTH - 10:
        game_over()

    # Проверка на столкновение с телом змейки
    for block in snake_body[1:]:
        if snake_position == block:
            game_over()

    # Отображение очков и уровня
    show_score_level()

    # Обновление экрана и контроль FPS
    pygame.display.update()
    fps.tick(snake_speed)
