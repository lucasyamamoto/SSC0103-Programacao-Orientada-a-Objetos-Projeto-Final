from pygame.locals import *

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


class Snake:
    def __init__(self, skin):
        self.snake = [(20, 20), (21, 20), (22, 20)]
        self.skin = skin
        self.direction = LEFT
        self.fast = False

    def listen(self, event):
        if event.key == K_UP:
            self.fast = False
            if self.direction == UP:
                self.fast = True
            if self.direction != DOWN:  # Para o snake nao voltar
                self.direction = UP

        if event.key == K_DOWN:
            self.fast = False
            if self.direction == DOWN:
                self.fast = True
            if self.direction != UP:
                self.direction = DOWN

        if event.key == K_LEFT:
            self.fast = False
            if self.direction == LEFT:
                self.fast = True
            if self.direction != RIGHT:
                self.direction = LEFT

        if event.key == K_RIGHT:
            self.fast = False
            if self.direction == RIGHT:
                self.fast = True
            if self.direction != LEFT:
                self.direction = RIGHT

    def collision(self, tup):
        return collision(self.snake[0], tup)

    def auto_collision(self):
        for ki, i in enumerate(self.snake):
            for kj, j in enumerate(self.snake):
                if kj == ki:
                    continue
                if collision(i, j):
                    return True
        return False

    def grow(self):
        self.snake.append((0, 0))

    def update(self):
        if self.auto_collision():
            self.snake = [(20, 20), (21, 20), (22, 20)]

        self.snake.pop()

        new_pos = ()
        if self.direction == UP:
            new_pos = (self.snake[0][0], (self.snake[0][1] - 1) % 60)
        if self.direction == DOWN:
            new_pos = (self.snake[0][0], (self.snake[0][1] + 1) % 60)
        if self.direction == RIGHT:
            new_pos = ((self.snake[0][0] + 1) % 60, self.snake[0][1])
        if self.direction == LEFT:
            new_pos = ((self.snake[0][0] - 1) % 60, self.snake[0][1])

        self.snake.insert(0, new_pos)

    def drawn(self, screen, ratio):
        for pos in self.snake:
            screen.blit(self.skin, (pos[0] * ratio, pos[1] * ratio))
