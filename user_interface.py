import random, sys, time, math, pygame
from pygame.locals import *
import numpy as np
import copy
import utils

# Window Information
FPS = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
TOP_MARGIN = 80
MARGIN = 50
GAMEBOARD_SIZE_COL = 8
GAMEBOARD_SIZE_ROW = 6
GRID_HEIGHT = WINDOW_WIDTH - 2 * (MARGIN)
GRID_WIDTH = WINDOW_HEIGHT - TOP_MARGIN - MARGIN

HALF_POSITION_WIDTH = float(GRID_WIDTH / (2*GAMEBOARD_SIZE_COL))
HALF_POSITION_HEIGHT = float(GRID_HEIGHT / (2*GAMEBOARD_SIZE_ROW))

# Colors
#				 R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (200,  72,  72)
LIGHT_ORANGE = (198, 108,  58)
ORANGE       = (180, 122,  48)
GREEN        = ( 72, 160,  72)
BLUE         = ( 66,  72, 200)
YELLOW       = (162, 162,  42)
NAVY         = ( 75,   0, 130)
PURPLE       = (143,   0, 255)
BADUK        = (220, 179,  92)

def Return_Num_Action():
    return GAMEBOARD_SIZE_COL * GAMEBOARD_SIZE_ROW

class GameState:
    def __init__(self):
        global DISPLAYSURF, BASIC_FONT, TITLE_FONT, GAMEOVER_FONT, ELEMENT_FONT
        pygame.init()
        
        DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Link Game')

        ELEMENT_FONT = pygame.font.SysFont('Arial', 64)
        BASIC_FONT = pygame.font.SysFont('Arial', 24)
        TITLE_FONT = pygame.font.SysFont('Arial', 36)
        GAMEOVER_FONT = pygame.font.SysFont('Arial', 48)

        # Set initial parameters
        self.gameboard = np.zeros([GAMEBOARD_SIZE_ROW, GAMEBOARD_SIZE_COL])
        self.dead_lock = False

        # List of X coordinates and Y coordinates
        self.X_coord = []
        self.Y_coord = []

        for i in range(GAMEBOARD_SIZE_COL):
            self.X_coord.append(
                MARGIN + i * float(GRID_WIDTH / (GAMEBOARD_SIZE_COL)) + float(
                    GRID_WIDTH / (GAMEBOARD_SIZE_COL * 4)))
        
        for i in range(GAMEBOARD_SIZE_ROW):
            self.Y_coord.append(
                TOP_MARGIN + i * float(GRID_HEIGHT / (GAMEBOARD_SIZE_ROW)) + float(
                    GRID_HEIGHT / (GAMEBOARD_SIZE_ROW * 4)))
    
    def set_board(self, game_board):
        self.gameboard = game_board

    # Draw main board
    def draw_main_board(self):

        #Vertical Lines
        for i in range(GAMEBOARD_SIZE_COL + 1):
            pygame.draw.line(DISPLAYSURF, WHITE, 
            (MARGIN + i * float(GRID_WIDTH/GAMEBOARD_SIZE_COL), TOP_MARGIN + GRID_HEIGHT),
            (MARGIN + i * float(GRID_WIDTH/GAMEBOARD_SIZE_COL), TOP_MARGIN), 1)

        #Horizontal Lines
        for i in range(GAMEBOARD_SIZE_ROW + 1):
            pygame.draw.line(DISPLAYSURF, WHITE,
            (MARGIN, TOP_MARGIN + i * float(GRID_HEIGHT/GAMEBOARD_SIZE_ROW)),
            (MARGIN + GRID_WIDTH, TOP_MARGIN + i * float(GRID_HEIGHT/GAMEBOARD_SIZE_ROW)), 1)

        # Draw marks
        for i in range(self.gameboard.shape[0]):
            for j in range(self.gameboard.shape[1]):
                if(int(self.gameboard[i][j]) != 0):
                    textSurf = ELEMENT_FONT.render(str(int(self.gameboard[i][j])), False, WHITE)
                    center = (self.X_coord[j], self.Y_coord[i])
                    DISPLAYSURF.blit(textSurf, center)
    
    def title_msg(self):
        """
        Output the title at the top left corner
        """
        titleSurf = TITLE_FONT.render('Game Board', False, WHITE)
        titleRect = titleSurf.get_rect()
        titleRect.topleft = (10, 30)
        DISPLAYSURF.blit(titleSurf, titleRect)

    def warning_msg(self):
        """
        Output the warning message at the top right corner
        """
        titleSurf = TITLE_FONT.render('Invalid Action', False, WHITE)
        titleRect = titleSurf.get_rect()
        titleRect.topright = (WINDOW_WIDTH - 50, 30)
        DISPLAYSURF.blit(titleSurf, titleRect)
        pygame.display.update()
    
    def terminate(self):
        """
        Terminate the game
        """
        pygame.quit()
        sys.exit()


    def get_clicked_element(self, mouse_pos):
        """
        Get the selected index when click mouse
        """
        x_index = -1
        y_index = -1
        for i in range(len(self.X_coord)):
            for j in range(len(self.Y_coord)):
                if (self.X_coord[i] - HALF_POSITION_WIDTH < mouse_pos[0] < self.X_coord[
                    i] + HALF_POSITION_WIDTH) and (self.Y_coord[j] - HALF_POSITION_HEIGHT < mouse_pos[1] <
                                            self.Y_coord[j] + HALF_POSITION_HEIGHT):
                    
                    x_index = i
                    y_index = j
        
        return((x_index, y_index))
    
    def checkStatus(self, index):
        """
        Return True if the index is valid, False otherwise
        
        Becareful with the index, for numpy array it will be array[y_index, x_index]
        """
        if index[0] == -1:
            return False
        if self.gameboard[index[1], index[0]] == 0:
            return False
        return True
    
    def checkElement(self, in1, in2):
        """
        Return True if two elements can be cancelled out, False otherwise
        """
        if in1 == in2:
            return False
        if not self.gameboard[in1[1],in1[0]] == self.gameboard[in2[1],in2[0]]:
            return False
        # Make the gameboard looks like
        # 0 0 0 0 0
        # 0 1 2 3 0
        # 0 4 0 4 0
        # 0 3 2 1 0
        # 0 0 0 0 0
        # that surrounding by 0 so that make it eaiser in check the path
        G = np.zeros([GAMEBOARD_SIZE_ROW+2, GAMEBOARD_SIZE_COL+2])
        G[1:GAMEBOARD_SIZE_ROW+1,1:GAMEBOARD_SIZE_COL+1] = self.gameboard
        return utils.DFS(G, (in1[0]+1, in1[1]+1), (in2[0]+1, in2[1]+1))

    def run(self, second_step = False, index = 0, warning = False):
        """
        Run the game
        """
        # Key settings
        mouse_pos = 0
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                self.terminate()
            elif pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()

        # Check mouse position and count
        if(second_step and mouse_pos != 0):
            warning = False
            new_index = self.get_clicked_element(mouse_pos)
            print("Received second element new click on ({},{})".format(new_index[0], new_index[1]))
            
            # check if the index valid
            if self.checkStatus(new_index):
                # check if cancellout out
                if self.checkElement(index, new_index):
                    self.gameboard[new_index[1],new_index[0]] = 0
                    self.gameboard[index[1],index[0]] = 0
                else:
                    warning = True
            else:
                warning = True
            index = 0
            second_step = False
        
        elif(mouse_pos != 0):
            warning = False
            index = self.get_clicked_element(mouse_pos)
            print("Received first element new click on ({},{})".format(index[0], index[1]))
            if self.checkStatus(index):
                second_step = True
            else:
                index = 0
                warning = True
                second_step = False


        # Fill background color
        DISPLAYSURF.fill(BLACK)

        # Draw board
        self.draw_main_board()

        # Display Information
        self.title_msg()

        #Display the warning message if needed
        if(warning): self.warning_msg()

        pygame.display.update()

        return second_step, index, warning, self.gameboard

def main():
    """
    Main function, will be moved to play.py
    """
    board = utils.BoardState(GAMEBOARD_SIZE_COL, GAMEBOARD_SIZE_ROW)
    board.generate_new_state()
    
    #Initial value
    second_step = False
    index = 0
    warning = False

    game = GameState()
    game.set_board(np.array(board.get_state()))

    while True:
        (second_step, index, warning, _) = game.run(second_step, index, warning)

if __name__ == '__main__':
    main()