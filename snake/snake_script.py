import pygame
import random
from pygame.locals import *
from snake import Snake
from apple import Apple

BLOCK_SIZE = 20   # Size of blocks
SCREEN_SIZE = 30  # The width and height of the screen in number of blocks
FONT_SIZE = 18


def mul(t, n):
    return (t[0] * n, t[1] * n)


def on_grid_random():
    x = random.randint(0, SCREEN_SIZE - 1)
    y = random.randint(0, SCREEN_SIZE - 1)
    return (x, y)


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE * BLOCK_SIZE, SCREEN_SIZE * BLOCK_SIZE))
pygame.display.set_caption('Snake')

snake_skin = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
snake_skin.fill((255, 255, 255))
snake = Snake(snake_skin, SCREEN_SIZE)


apple_sprite = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
apple_sprite.fill((255, 0, 0))
apple = Apple(
    apple_sprite,  # sprite
    on_grid_random(),  # pos
    14,  # num
    pygame.font.SysFont("arial", FONT_SIZE)  # font
)

clock = pygame.time.Clock()

while True:
    clock.tick(30 if snake.fast else 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        if event.type == KEYDOWN:
            snake.listen(event)

    if snake.collision(apple.pos):
        apple.change(on_grid_random(), random.randint(0, 99))
        snake.grow()

    snake.update()

    screen.fill((0, 0, 0))

    apple.drawn(screen, 20)
    snake.drawn(screen, BLOCK_SIZE)

    pygame.display.update()
