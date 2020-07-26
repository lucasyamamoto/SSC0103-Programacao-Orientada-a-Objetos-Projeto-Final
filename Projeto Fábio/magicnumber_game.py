import pygame
from pygame.locals import *
import numpy as np
from random import *

N  = 3
magic_square = np.zeros((N,N), dtype=int)

aleatory = randint(0, 100)

actualPlay = 1  + aleatory

grid = [ [ None, None, None ], 
         [ None, None, None ],
         [ None, None, None ] ]

win = None

width = 600
height = 525
padding = 0

def restartGame(board):
    global magic_square,aleatory,N,actualPlay,win,grid
    board.fill ((250, 250, 250))

    distw = (int) (width/3) - padding
    disth = (int) (height) - padding
    
    pygame.draw.line (board, (0,0,0), (distw, padding), (distw, disth), 2)
    pygame.draw.line (board, (0,0,0), (2*distw,padding), (2*distw, disth), 2)

    distw = (int) (width) - padding
    disth = (int) (height/3) - padding

    pygame.draw.line (board, (0,0,0), (padding, disth), (distw, disth), 2)
    pygame.draw.line (board, (0,0,0), (padding, 2*disth), (distw, 2*disth), 2)

    N  = 3
    magic_square = np.zeros((N,N), dtype=int)

    grid = [ [ None, None, None ], 
         [ None, None, None ],
         [ None, None, None ] ]

    aleatory = randint(0, 100)

    actualPlay = 1  + aleatory

    win = None


def initBoard(ttt):

    background = pygame.Surface (ttt.get_size())
    background = background.convert()
    background.fill ((250, 250, 250))

    distw = (int) (width/3) - padding
    disth = (int) (height) - padding
    
    pygame.draw.line (background, (0,0,0), (distw, padding), (distw, disth), 2)
    pygame.draw.line (background, (0,0,0), (2*distw,padding), (2*distw, disth), 2)

    distw = (int) (width) - padding
    disth = (int) (height/3) - padding

    pygame.draw.line (background, (0,0,0), (padding, disth), (distw, disth), 2)
    pygame.draw.line (background, (0,0,0), (padding, 2*disth), (distw, 2*disth), 2)

    return background

def makesSquare():
    global magic_square,aleatory
    
    n = 1
    i, j = 0, N//2

    while n <= N**2:
        magic_square[i, j] = n
        n += 1
        newi, newj = (i-1) % N, (j+1)% N
        if magic_square[newi, newj]:
            i += 1
        else:
            i, j = newi, newj

    for i in range(3):
        for j in range(3):
            magic_square[i][j] += aleatory
    print("Numero Aleatorio: " + str(aleatory))
    print(magic_square)
    
def drawStatus (board):

    global win,actualPlay
    message1 = "A soma de cada linha será: " + str((3*aleatory)+15)
    message2 = ""
    if(win!=None):
        if(win):
            message2 = "Você Ganhou"
        else:
            message2 = "Você Perdeu"
    else:
        message2 += "Clique no lugar onde irá o número " + str(actualPlay)

    fontsize = 45
    font = pygame.font.Font(None, fontsize)
    text1 = font.render(message1, True, (10, 10, 10))
    text2 = font.render(message2, True, (10, 10, 10))

    distw = (int) (10)
    disth = (int) (height) + 50

    board.fill ((250, 250, 250), (0, 500, 600, 200))
    board.blit(text1, (distw, disth))
    board.blit(text2, (distw, disth+50))
    return

def showBoard (ttt, board):

    drawStatus (board)
    ttt.blit (board, (0, 0))
    pygame.display.flip()
    
def boardPos (mouseX, mouseY):
    distw = (int) (width/3) - padding
    disth = (int) (height/3) - padding

    if (mouseY < disth):
        row = 0
    elif (mouseY < 2*disth):
        row = 1
    else:
        row = 2

    if (mouseX < distw):
        col = 0
    elif (mouseX < 2*distw):
        col = 1
    else:
        col = 2

    return (row, col)

def drawMove (board, boardRow, boardCol, Piece):
    global grid, actualPlay

    distw = (int) (width/3) - padding
    disth = (int) (height/3) - padding

    centerX = (int) (((boardCol) * distw) + (distw/2))
    centerY = (int) (((boardRow) * disth) + (disth/2))
    fontsize = 90
    font = pygame.font.Font(None, fontsize)
    text = font.render(str(actualPlay), True, (10, 10, 10))

    #board.fill ((250, 250, 250), (0, 300, 300, 25))
    board.blit(text, (centerX-20, centerY-20))

    grid [boardRow][boardCol] = Piece
    
def clickBoard(board):

    global grid, actualPlay
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    if(mouseY > height or mouseX > width):
        return

    (row, col) = boardPos(mouseX, mouseY)

    if ((grid[row][col] != None)):
        return

    print(str(row) +  " " + str(col))
    
    drawMove (board, row, col, actualPlay)

    actualPlay+=1
    
def gameWon(board):
    global grid, win,actualPlay,magic_square

    if((actualPlay) < (aleatory+10) or win != None):
        return

    for i in range(3):
        for j in range(3):
            if(grid[i][j] != magic_square[i][j]):
                win = False
                return
    win = True
    return

# --------------------------------------------------------------------
pygame.init()
ttt = pygame.display.set_mode ((width,height + 200))
pygame.display.set_caption ('Número Mágico')
makesSquare()

board = initBoard (ttt)

running = 1

while (running == 1):
    for event in pygame.event.get():
        if event.type is QUIT:
            running = 0
        elif event.type is MOUSEBUTTONDOWN:
            clickBoard(board)
        elif event.type is KEYDOWN:
            if event.key == pygame.K_r:
                restartGame(board)
                makesSquare()
                
        gameWon (board)
        showBoard (ttt, board)

pygame.quit()
