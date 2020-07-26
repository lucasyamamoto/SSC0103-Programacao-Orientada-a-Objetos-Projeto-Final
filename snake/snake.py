import pygame
from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


class Snake:
    """
    This class is responsible for the creation and update of the Snake Object
    """
    def __init__(self, skin, SCREEN_SIZE):
        self.SCREEN_SIZE = SCREEN_SIZE
        self.snake = [(20, 20), (21, 20), (22, 20)]
        self.skin = skin
        self.direction = LEFT
        self.fast = False
        self.counter = 0
    def listen(self, event):
        """
        This method receives a key from a event, then move the snake
        :param event:
        :return:
        list : Snake new position
        """
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
        """
            This method verify if a collision have occurred
            :param c1: Snake's head
            :param c2: Apple position
            :return:
            Boolean: Colision
            """
        return (self.snake[0][0] == tup[0]) and (self.snake[0][1] == tup[1])

    def auto_collision(self):
        """
        This method verify the auto collision of the snake
        :return:
        Boolean: Auto collision
        """
        for i in self.snake[1:]:
            if self.collision(i):
                return True

        return False
    def boundry_collision(self):
        """
        This method verify if the snake head collide with the borders of the screen
        :return:
        Boolean: Collision
        """
        if self.snake[0][0] == 29 or self.snake[0][1] == 29 or self.snake[0][0] < 0 or self.snake[0][1] < 0:
            return True

    def grow(self): # Add a block on snake
        """
        This method make the snake bigger after eating a apple
        :return:
        """
        self.snake.append((0, 0))

    def update(self):
        """
        This method update the actual state of the snake, and verify if it has a collision
        :return:
        """
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
        """
        This method draws the snake on the screen
        :param screen: screen obj from pygame
        :param size: screen size
        :return:
        """
        for pos in self.snake:
            screen.blit(self.skin, (pos[0] * size, pos[1] * size))

    def snake_reset(self):
        """
        This method resets the snake position, score and size when eat the wrong apple
        :return:
        """
        self.snake = [(20, 20), (21, 20), (22, 20)]
        self.direction = LEFT
        self.fast = False
        self.counter = 0