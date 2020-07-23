import pygame
import random
from pygame.locals import *
from snake import Snake

BLOCK = 10


def mul(t, n):
    return (t[0] * n, t[1] * n)


def on_grid_random():
    x = random.randint(0, 59)
    y = random.randint(0, 59)
    return (x, y)


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))

snake = Snake(snake_skin)

apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))


clock = pygame.time.Clock()

while True:
    clock.tick(30 if snake.fast else 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            snake.listen(event)

    if snake.collision(apple_pos):
        apple_pos = on_grid_random()
        snake.grow()

    snake.update()

    screen.fill((0, 0, 0))
    screen.blit(apple, (apple_pos[0] * 10, apple_pos[1] * 10))
    snake.drawn(screen, 10)

    pygame.display.update()
