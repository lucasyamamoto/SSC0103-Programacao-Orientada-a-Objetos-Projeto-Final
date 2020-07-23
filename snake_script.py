import pygame
import random
from pygame.locals import *
from snake import Snake
from apple import Apple

BLOCK_SIZE = 20   # Size of blocks
SCREEN_SIZE = 30  # The width and height of the screen in number of blocks
FONT_SIZE = 18
PRIME_NUMBERS = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
Counter = 0
tutorial1 = """Geraldo é uma cobrinha sapeka e que vive faminta. Sua comida favorita é a fruta maça."""
tutorial2 = """Porém Geraldo é bem especifico, ele só come maçãs que são de numero primo no pé."""
tutorial3 = """INSTRUÇÔES"""
tutorial4 = """Para isso ajude Geraldo a se alimentar capturando apenas as  maçãs com numeros primos"""
tutorial5 = """E utilizando as setas do teclado para se mover"""


def mul(t, n):
    return (t[0] * n, t[1] * n)


def on_grid_random():
    x = random.randint(0, SCREEN_SIZE - 2)
    y = random.randint(0, SCREEN_SIZE - 2)
    return (x, y)


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def prime_apple_randomizer():
    number = random.choice(PRIME_NUMBERS)

    return int(number)
def normal_apple_randomizer():
    number = random.randint(0 ,99)
    while number in PRIME_NUMBERS:
        number = random.randint(0, 99)
    return number

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE * BLOCK_SIZE, SCREEN_SIZE * BLOCK_SIZE))
pygame.display.set_caption('Snake')
##### MENU ########################
score_font = pygame.font.Font('freesansbold.ttf', 13)
score_screen = score_font.render(f'{tutorial1}', True, (255, 255, 255))
score_rect = score_screen.get_rect()
score_rect.midtop = (600 / 2, 10)
screen.blit(score_screen, score_rect)
score_font = pygame.font.Font('freesansbold.ttf', 13)
score_screen = score_font.render(f'{tutorial2}', True, (255, 255, 255))
score_rect = score_screen.get_rect()
score_rect.midtop = (600 / 2, 50)
screen.blit(score_screen, score_rect)
score_font = pygame.font.Font('freesansbold.ttf', 13)
score_screen = score_font.render(f'{tutorial3}', True, (255, 255, 255))
score_rect = score_screen.get_rect()
score_rect.midtop = (600 / 2, 100)
screen.blit(score_screen, score_rect)
score_font = pygame.font.Font('freesansbold.ttf', 13)
score_screen = score_font.render(f'{tutorial4}', True, (255, 255, 255))
score_rect = score_screen.get_rect()
score_rect.midtop = (600 / 2, 150)
screen.blit(score_screen, score_rect)
score_font = pygame.font.Font('freesansbold.ttf', 13)
score_screen = score_font.render(f'{tutorial5}', True, (255, 255, 255))
score_rect = score_screen.get_rect()
score_rect.midtop = (600 / 2, 200)
screen.blit(score_screen, score_rect)
pygame.display.update()
pygame.time.wait(9000)

snake_skin = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
snake_skin.fill((255, 255, 255))
snake = Snake(snake_skin, SCREEN_SIZE)


prime_apple_sprite = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
prime_apple_sprite.fill((255, 0, 0))
prime_apple = Apple(
    prime_apple_sprite,  # sprite
    on_grid_random(),  # pos
    prime_apple_randomizer(),  # num
    pygame.font.SysFont("arial", FONT_SIZE)  # font
)
normal_apple_sprite = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
normal_apple_sprite.fill((255, 0, 0))
normal_apple = Apple(
    normal_apple_sprite,  # sprite
    on_grid_random(),  # pos
    normal_apple_randomizer(),  # num
    pygame.font.SysFont("arial", FONT_SIZE)  # font
)
clock = pygame.time.Clock()


while True:
    clock.tick(30 if snake.fast else 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            snake.listen(event)




    if snake.collision(prime_apple.pos):
        prime_apple.change(on_grid_random(), prime_apple_randomizer())
        normal_apple.change(on_grid_random(), normal_apple_randomizer())
        snake.grow()
        Counter = Counter + 1

    if snake.collision(normal_apple.pos):
        snake.snake_reset()
        prime_apple.change(on_grid_random(), prime_apple_randomizer())
        normal_apple.change(on_grid_random(), normal_apple_randomizer())

    if snake.boundry_collision():# Check the collision with boudaries
        game_over = True
        break

    snake.update()

    screen.fill((0, 0, 0))

    prime_apple.drawn(screen, 20)
    normal_apple.drawn(screen, 20)
    snake.drawn(screen, BLOCK_SIZE)

    pygame.display.update()

while True:
        game_over_font = pygame.font.Font('freesansbold.ttf', 75)
        game_over_screen = game_over_font.render(f'Game Over', True, (255, 255, 255))
        game_over_rect = game_over_screen.get_rect()
        game_over_rect.midtop = (600 / 2, 10)
        screen.blit(game_over_screen, game_over_rect)
        score_font = pygame.font.Font('freesansbold.ttf', 30)
        score_screen = score_font.render(f'Pontuação final: {Counter}', True, (255, 255, 255))
        score_rect = score_screen.get_rect()
        score_rect.midtop = (600 / 2, 100)
        screen.blit(score_screen, score_rect)
        pygame.display.update()
        pygame.time.wait(500)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()