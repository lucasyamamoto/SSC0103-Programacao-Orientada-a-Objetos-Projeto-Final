import pygame
import random
from pygame.locals import *
from snake.snake import Snake
from snake.apple import Apple
"""
Created by Igor Lovatto Resende
N USP 10439099
"""

class SnakeGame:
    FONT_SIZE = 18
    PRIME_NUMBERS = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    BLOCK_SIZE = 20   # Size of blocks

    def __init__(self, screen_size):
        self.screen_size = screen_size // self.BLOCK_SIZE  # The width and height of the screen in number of blocks
    
    def mul(self, t, n):
        return (t[0] * n, t[1] * n)

    def on_grid_random(self):
        """
        This function calculate a random position for a object on the screen

        :returns:
        tuple: Random position
        """
        x = random.randint(0, self.screen_size - 2)
        y = random.randint(0, self.screen_size - 2)
        return (x, y)


    def collision(self, c1, c2):

        return (c1[0] == c2[0]) and (c1[1] == c2[1])

    def prime_apple_randomizer(self):
        """
        This function choose a random prime number from the self.PRIME_NUMBERS list
        :return:
        int: Random prime number
        """
        number = random.choice(self.PRIME_NUMBERS)

        return int(number)

    def normal_apple_randomizer(self):
        """
        This function chosse a not-prime random number between 0 and 99
        :return:
        int:
        """
        number = random.randint(0 ,99)
        while number in self.PRIME_NUMBERS:
            number = random.randint(0, 99)
        return number

    def main(self, screen):
        screen.fill((0, 0, 0))
        tutorial1 = """Geraldo é uma cobrinha sapeca e que vive faminta. Sua comida favorita é a fruta maça."""
        tutorial2 = """Porém Geraldo é bem especifico, ele só come maçãs que são de numero primo no pé."""
        tutorial3 = """INSTRUÇÔES"""
        tutorial4 = """Para isso ajude Geraldo a se alimentar capturando apenas as  maçãs com numeros primos"""
        tutorial5 = """E utilizando as setas do teclado para se mover"""

        ##### TUTORIAL ########################
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

        snake_skin = pygame.Surface((self.BLOCK_SIZE, self.BLOCK_SIZE))
        snake_skin.fill((255, 255, 255))
        self.snake = Snake(snake_skin, self.screen_size)


        prime_apple_sprite = pygame.Surface((self.BLOCK_SIZE, self.BLOCK_SIZE))
        prime_apple_sprite.fill((255, 0, 0))
        prime_apple = Apple(
            prime_apple_sprite,  # sprite
            self.on_grid_random(),  # pos
            self.prime_apple_randomizer(),  # num
            pygame.font.SysFont("arial", self.FONT_SIZE)  # font
        )
        normal_apple_sprite = pygame.Surface((self.BLOCK_SIZE, self.BLOCK_SIZE))
        normal_apple_sprite.fill((255, 0, 0))
        normal_apple = Apple(
            normal_apple_sprite,  # sprite
            self.on_grid_random(),  # pos
            self.normal_apple_randomizer(),  # num
            pygame.font.SysFont("arial", self.FONT_SIZE)  # font
        )
        clock = pygame.time.Clock()

        while True:
            """
            This is the main looping of the game, resposible for update the screen,snake and apples
            """
            clock.tick(10 if self.snake.fast else 5)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

                if event.type == KEYDOWN:
                    self.snake.listen(event)
                    if event.key == K_ESCAPE:
                        return

            if self.snake.collision(prime_apple.pos):
                prime_apple.change(self.on_grid_random(), self.prime_apple_randomizer())
                normal_apple.change(self.on_grid_random(), self.normal_apple_randomizer())
                self.snake.grow()
                self.snake.counter = self.snake.counter+ 1

            if self.snake.collision(normal_apple.pos):
                self.snake.snake_reset()
                prime_apple.change(self.on_grid_random(), self.prime_apple_randomizer())
                normal_apple.change(self.on_grid_random(), self.normal_apple_randomizer())

            if self.snake.boundry_collision():# Check the collision with boudaries
                game_over = True
                self.game_over_screen(screen)
                return

            self.snake.update()

            screen.fill((0, 0, 0))

            prime_apple.drawn(screen, 20)
            normal_apple.drawn(screen, 20)
            self.snake.drawn(screen, self.BLOCK_SIZE)

            pygame.display.update()

    def game_over_screen(self, screen):
        """
        This is the Game over menu looping. Responsible for the game-over screen and score
        """
        while True:
            game_over_font = pygame.font.Font('freesansbold.ttf', 75)
            game_over_screen = game_over_font.render(f'Game Over', True, (255, 255, 255))
            game_over_rect = game_over_screen.get_rect()
            game_over_rect.midtop = (600 / 2, 10)
            screen.blit(game_over_screen, game_over_rect)
            score_font = pygame.font.Font('freesansbold.ttf', 30)
            score_screen = score_font.render(f'Pontuação final: {self.snake.counter}', True, (255, 255, 255))
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
                    elif event.type == KEYDOWN:
                        if event.key == K_RETURN or event.key == K_KP_ENTER:
                            self.main(screen)
                        elif event.key == K_ESCAPE:
                            return

if __name__ == '__main__':
    pygame.init()
    screen_size = 20
    block_size = 30
    screen = pygame.display.set_mode((screen_size * block_size, screen_size * block_size))
    pygame.display.set_caption('Snake')
    game = SnakeGame(screen_size * block_size)
    game.main(screen)
    pygame.quit()
    exit()
