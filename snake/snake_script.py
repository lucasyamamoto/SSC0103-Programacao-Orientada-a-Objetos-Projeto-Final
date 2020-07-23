import pygame
import random
from pygame.locals import *
from snake import Snake

BLOCK_SIZE = 20   # Size of blocks
SCREEN_SIZE = 30  # The width and height of the screen in number of blocks


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

font = pygame.font.SysFont("arial", BLOCK_SIZE - 1)

apple_pos = on_grid_random()
apple = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
apple.fill((255, 0, 0))
apple_num = 14
apple_text = font.render(str(apple_num), 1, (255,255,0))

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
    screen.blit(apple, (apple_pos[0] * BLOCK_SIZE, apple_pos[1] * BLOCK_SIZE))
    screen.blit(apple_text, (apple_pos[0] * BLOCK_SIZE, apple_pos[1] * BLOCK_SIZE))
    snake.drawn(screen, BLOCK_SIZE)

    pygame.display.update()
