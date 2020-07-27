import pygame
from pygame.locals import *
from NUMBERS.magicnumber_game import MagicNumber
from equation.equation import Equation
from snake.snake_script import SnakeGame


BACKGROUND = (200, 200, 200)
FOREGROUND = (0, 0, 0)
SELECTED = (0, 255, 200)

class MenuItem:
    """A item of menu"""

    def __init__(self, option:str, image:pygame.Surface, font:pygame.font.Font, size:tuple=(600, 150), pos:tuple=(0, 0)) -> None:
        """Constructor of MenuItem"""

        self.option = option
        self.pos = pos
        self.size = size

        self.image = pygame.transform.scale(image, (self.size[1] - 10, self.size[1] - 10))
        self.font = font
        self.rect1 =  pygame.Rect(self.pos, self.size)
        self.rect2 =  pygame.Rect((self.pos[0] + 4, self.pos[1] + 4),
                                  (self.size[0] - 8, self.size[1] - 8))

    def collision(self, tup: tuple) -> None:
        """Test collision with a point"""

        return (
            self.pos[0] < tup[0] < self.pos[0] + self.size[0] and
            self.pos[1] < tup[1] < self.pos[1] + self.size[1]
        )

    def drawn(self, screen:pygame.Surface, selected:bool=False):
        """
        Drawn the menu item on screen
        :param selected: If true, the border will be drawn with other color
        """

        border_color = SELECTED if selected else FOREGROUND
        pygame.draw.rect(screen, border_color, self.rect1)
        pygame.draw.rect(screen, BACKGROUND, self.rect2)

        screen.blit(self.image, (self.pos[0] + 5, self.pos[1] + 5))

        # x is after the image
        # y is the middle of MenuItem
        x = self.size[1] + 40
        y = self.size[1] // 2 - (self.font.size(self.option)[1] // 2)
        x += self.pos[0]
        y += self.pos[1]

        text = self.font.render(self.option, True, FOREGROUND)
        screen.blit(text, (x, y))




class Menu:
    """Menu class"""

    def __init__(self, screen:pygame.Surface):
        """Constructor of Menu"""

        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 50)

        font = pygame.font.Font('freesansbold.ttf', 36)
        self.options = [ 
            MenuItem(
                'Snake',
                pygame.image.load('images/snake.png'),
                font,
                pos=(0, 150)
            ),
            MenuItem(
                'Equation',
                pygame.image.load('images/equation.png'),
                font,
                pos=(0, 300)
            ),
            MenuItem(
                'Magic Numbers',
                pygame.image.load('images/equation.png'),
                font,
                pos=(0, 450)
            ),
        ]
        

    def main(self):
        """Drawn the menu"""

        while True:
            self.clock.tick(40)
            screen.fill(BACKGROUND)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    if self.options[0].collision(pygame.mouse.get_pos()):
                        # Snake
                        self.screen = pygame.display.set_mode((600, 600))
                        pygame.display.set_caption ('Snake')
                        
                        game = SnakeGame(600)
                        game.main(self.screen)
                        self.screen = pygame.display.set_mode((600, 600))


                    elif self.options[1].collision(pygame.mouse.get_pos()):
                        # Equation
                        self.screen = pygame.display.set_mode((800, 600))
                        pygame.display.set_caption ('Equation')

                        game = Equation(self.screen)
                        game.main()
                        self.screen = pygame.display.set_mode((600, 600))

                    elif self.options[2].collision(pygame.mouse.get_pos()):
                        # Numbers
                        self.screen = pygame.display.set_mode((600, 725))
                        pygame.display.set_caption ('Magic Numbers')

                        game = MagicNumber()
                        game.main(self.screen)
                        self.screen = pygame.display.set_mode((600, 600))
                        

            text = 'Menu'
            (w, h) = self.font.size(text)
            x = 300 - w // 2
            y = 15
            text = self.font.render(text, True, FOREGROUND)
            screen.blit(text, (x, y))

            for i in self.options:
                if i.collision(pygame.mouse.get_pos()):
                    i.drawn(screen, selected=True)
                else:
                    i.drawn(screen)
            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Menu')

    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))

    menu = Menu(screen)
    menu.main()
    pygame.quit()
