import pygame
from pygame.locals import *
import numpy as np
from random import *

class MagicNumber:
    N  = 3
    
    def __init__(self):
        self.magic_square = np.zeros((self.N,self.N), dtype=int)

        self.aleatory = randint(0, 100)

        self.actualPlay = 1  + self.aleatory

        self.grid = [ [ None, None, None ], 
                      [ None, None, None ],
                      [ None, None, None ] ]

        self.win = None

        self.width = pygame.display.get_surface().get_width()
        self.height = pygame.display.get_surface().get_height() - 200
        self.padding = 0

    def restartGame(self, board):
        board.fill ((250, 250, 250))

        distw = (int) (self.width/3) - self.padding
        disth = (int) (self.height) - self.padding
    
        pygame.draw.line (board, (0,0,0), (distw, self.padding), (distw, disth), 2)
        pygame.draw.line (board, (0,0,0), (2*distw,self.padding), (2*distw, disth), 2)

        distw = (int) (self.width) - self.padding
        disth = (int) (self.height/3) - self.padding

        pygame.draw.line (board, (0,0,0), (self.padding, disth), (distw, disth), 2)
        pygame.draw.line (board, (0,0,0), (self.padding, 2*disth), (distw, 2*disth), 2)

        self.N  = 3
        self.magic_square = np.zeros((self.N,self.N), dtype=int)

        self.grid = [ [ None, None, None ], 
                 [ None, None, None ],
                 [ None, None, None ] ]

        self.aleatory = randint(0, 100)

        self.actualPlay = 1  + self.aleatory

        self.win = None


    def initBoard(self, ttt):

        background = pygame.Surface (ttt.get_size())
        background = background.convert()
        background.fill ((250, 250, 250))

        distw = (int) (self.width/3) - self.padding
        disth = (int) (self.height) - self.padding
    
        pygame.draw.line (background, (0,0,0), (distw, self.padding), (distw, disth), 2)
        pygame.draw.line (background, (0,0,0), (2*distw,self.padding), (2*distw, disth), 2)

        distw = (int) (self.width) - self.padding
        disth = (int) (self.height/3) - self.padding

        pygame.draw.line (background, (0,0,0), (self.padding, disth), (distw, disth), 2)
        pygame.draw.line (background, (0,0,0), (self.padding, 2*disth), (distw, 2*disth), 2)

        return background

    def makesSquare(self):
        n = 1
        i, j = 0, self.N//2

        while n <= self.N**2:
            self.magic_square[i, j] = n
            n += 1
            newi, newj = (i-1) % self.N, (j+1)% self.N
            if self.magic_square[newi, newj]:
                i += 1
            else:
                i, j = newi, newj

        for i in range(3):
            for j in range(3):
                self.magic_square[i][j] += self.aleatory
        print("Numero Aleatorio: " + str(self.aleatory))
        print(self.magic_square)
    
    def drawStatus (self, board):

        message1 = "A soma de cada linha será: " + str((3*self.aleatory)+15)
        message2 = ""
        if(self.win!=None):
            if(self.win):
                message2 = "Você Ganhou"
            else:
                message2 = "Você Perdeu"
        else:
            message2 += "Clique no lugar onde irá o número " + str(self.actualPlay)

        fontsize = 45
        font = pygame.font.Font(None, fontsize)
        text1 = font.render(message1, True, (10, 10, 10))
        text2 = font.render(message2, True, (10, 10, 10))

        distw = (int) (10)
        disth = (int) (self.height) + 50

        board.fill ((250, 250, 250), (0, 500, 600, 200))
        board.blit(text1, (distw, disth))
        board.blit(text2, (distw, disth+50))
        return

    def showBoard (self, ttt, board):

        self.drawStatus (board)
        ttt.blit (board, (0, 0))
        pygame.display.flip()
    
    def boardPos (self, mouseX, mouseY):
        distw = (int) (self.width/3) - self.padding
        disth = (int) (self.height/3) - self.padding

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

    def drawMove (self, board, boardRow, boardCol, Piece):
        distw = (int) (self.width/3) - self.padding
        disth = (int) (self.height/3) - self.padding

        centerX = (int) (((boardCol) * distw) + (distw/2))
        centerY = (int) (((boardRow) * disth) + (disth/2))
        fontsize = 90
        font = pygame.font.Font(None, fontsize)
        text = font.render(str(self.actualPlay), True, (10, 10, 10))

        #board.fill ((250, 250, 250), (0, 300, 300, 25))
        board.blit(text, (centerX-20, centerY-20))

        self.grid [boardRow][boardCol] = Piece
    
    def clickBoard(self, board):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        if(mouseY > self.height or mouseX > self.width):
            return

        (row, col) = self.boardPos(mouseX, mouseY)

        if ((self.grid[row][col] != None)):
            return

        print(str(row) +  " " + str(col))
    
        self.drawMove (board, row, col, self.actualPlay)

        self.actualPlay+=1
    
    def gameWon(self, board):
        if((self.actualPlay) < (self.aleatory+10) or self.win != None):
            return

        for i in range(3):
            for j in range(3):
                if(self.grid[i][j] != self.magic_square[i][j]):
                    self.win = False
                    return
        self.win = True
        return

    def main(self, ttt):
        self.makesSquare()

        board = self.initBoard (ttt)

        running = True


        while running:
            ttt.fill((250,250,250))
            for event in pygame.event.get():
                if event.type is QUIT:
                    running = False
                elif event.type is MOUSEBUTTONDOWN:
                    self.clickBoard(board)
                elif event.type is KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restartGame(board)
                        self.makesSquare()
                
            self.gameWon (board)
            self.showBoard (ttt, board)
            pygame.display.update()


# --------------------------------------------------------------------

if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 525
    ttt = pygame.display.set_mode ((width,height + 200))
    pygame.display.set_caption ('Número Mágico')

    game = MagicNumber()
    game.main(ttt)

    pygame.quit()
