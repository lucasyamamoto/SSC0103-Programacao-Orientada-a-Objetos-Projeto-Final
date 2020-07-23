import pygame, random
from pygame.locals import *

BLOCK = 10

def mul(t, n):
    return (t[0] * n, t[1] * n)

def on_grid_random():
    x = random.randint(0,59 * BLOCK)
    y = random.randint(0,59 * BLOCK)
    return (x//BLOCK, y//BLOCK)

def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def snake_self_collision(snake):
    for ki, i in enumerate(snake):
        for kj, j in enumerate(snake):
            if kj == ki:
                continue
            if collision(i, j):
                return True
    return False


def moviment(my_direction,snake):
    if my_direction == UP:
        snake[0] = (snake[0][0], (snake[0][1] - 1) % 60)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], (snake[0][1] + 1) % 60)
    if my_direction == RIGHT:
        snake[0] = ((snake[0][0] + 1)%60, snake[0][1])
    if my_direction == LEFT:
        snake[0] = ((snake[0][0] - 1)%60, snake[0][1])
    return snake

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Snake')

snake = [(20, 20), (21, 20), (22,20)]
snake_skin = pygame.Surface((10,10))
snake_skin.fill((255,255,255))

apple_pos = on_grid_random()
apple = pygame.Surface((10,10))
apple.fill((255,0,0))

my_direction = LEFT

clock = pygame.time.Clock()

fast = False
while True:
    clock.tick(30 if fast else 10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                fast = False
                if my_direction == UP:
                    fast = True
                if my_direction != DOWN:  # Para o snake nao voltar
                    my_direction = UP
            
            if event.key == K_DOWN:
                fast = False
                if my_direction == DOWN:
                    fast = True
                if my_direction != UP:
                    my_direction = DOWN
            
            if event.key == K_LEFT:
                fast = False
                if my_direction == LEFT:
                    fast = True
                if my_direction != RIGHT:
                    my_direction = LEFT
                
            
            if event.key == K_RIGHT:
                fast = False
                if my_direction == RIGHT:
                    fast = True
                if my_direction != LEFT:
                    my_direction = RIGHT


    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0,0))

    if snake_self_collision(snake):
        snake = [snake[0], snake[1], snake[2]]

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])

    snake = moviment(my_direction,snake)

    screen.fill((0,0,0))
    screen.blit(apple, mul(apple_pos, 10))
    for pos in snake:
        screen.blit(snake_skin,mul(pos, 10))

    pygame.display.update()