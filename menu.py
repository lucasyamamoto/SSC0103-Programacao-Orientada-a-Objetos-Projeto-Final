import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_caption('Menu')

screen = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

options = ['Snake', 'Equation', 'Sudoku']
selected = 0

font = pygame.font.Font('freesansbold.ttf', 18)
bigfont = pygame.font.Font('freesansbold.ttf', 36)

while True:
    clock.tick(10)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                selected -= 1
                selected = selected if selected >= 0 else len(options) - 1

            if event.key == K_DOWN:
                selected += 1
                selected = selected if selected < len(options) else 0

    x = 300 - bigfont.size('Menu')[0]//2
    y = 50
    text = bigfont.render('Menu', True, (255, 255, 255))
    screen.blit(text, (x, y))
    y += bigfont.size('Menu')[1] + 50

    x = 50
    for (index, op) in enumerate(options):
        op = ('>' if selected == index else ' ') + op
        text = font.render(op, True, (255, 255, 255))
        screen.blit(text, (x, y))

        y += font.size(op)[1]

    pygame.display.update()
        