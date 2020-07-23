import pygame
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Snake:
    def __init__(self, skin, SCREEN_SIZE):
        self.SCREEN_SIZE = SCREEN_SIZE
        self.snake = [(20, 20), (21, 20), (22, 20)]
        self.skin = skin
        self.direction = LEFT
        self.fast = False

    def listen(self, event):
        if event.key == K_UP:
            self.fast = False
            if self.direction == UP:
                self.fast = True
            if self.direction != DOWN:  # Para o snake nao dar meia volta
                self.direction = UP

        elif event.key == K_DOWN:
            self.fast = False
            if self.direction == DOWN:
                self.fast = True
            if self.direction != UP:
                self.direction = DOWN

        elif event.key == K_LEFT:
            self.fast = False
            if self.direction == LEFT:
                self.fast = True
            if self.direction != RIGHT:
                self.direction = LEFT

        elif event.key == K_RIGHT:
            self.fast = False
            if self.direction == RIGHT:
                self.fast = True
            if self.direction != LEFT:
                self.direction = RIGHT

    def collision(self, tup): # Test collision with the head of snake
        return (self.snake[0][0] == tup[0]) and (self.snake[0][1] == tup[1])

    def auto_collision(self):
        for i in self.snake[1:]:
            if self.collision(i):
                return True

        return False
    def boundry_collision(self):
        if self.snake[0][0] == 29 or self.snake[0][1] == 29 or self.snake[0][0] < 0 or self.snake[0][1] < 0:
            return True

    def grow(self): # Add a block on snake
        self.snake.append((0, 0))

    def update(self):
        if self.auto_collision():
            self.snake_reset()

        self.snake.pop()


        new_pos = ()
        if self.direction == UP:
            new_pos = (self.snake[0][0], (self.snake[0][1] - 1) % self.SCREEN_SIZE)
        if self.direction == DOWN:
            new_pos = (self.snake[0][0], (self.snake[0][1] + 1) % self.SCREEN_SIZE)
        if self.direction == RIGHT:
            new_pos = ((self.snake[0][0] + 1) % self.SCREEN_SIZE, self.snake[0][1])
        if self.direction == LEFT:
            new_pos = ((self.snake[0][0] - 1) % self.SCREEN_SIZE, self.snake[0][1])

        if self.boundry_collision():
            return True

        self.snake.insert(0, new_pos)

    def drawn(self, screen, size):
        
        for pos in self.snake:
            screen.blit(self.skin, (pos[0] * size, pos[1] * size))

    def snake_reset(self):
        self.snake = [(20, 20), (21, 20), (22, 20)]
        self.direction = LEFT
        self.fast = False
