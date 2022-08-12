#!/usr/bin/env python
# This is a simple python program that will solve a given Sudoku board using a backtracking algorithm.
# In addition, a GUI is provided, its purpose is to represent the Sudoku board and allow the user to
# press a "solve" button to see the before and after.

from cmath import rect
import winsound
import pygame
import pygame_gui
import time
pygame.font.init()

# Global variable to store the final result of the algorithm
fb = []

# Backtracking algorithm to fill the board
def fill(bo):
    # Base case, if the board is full then fill the global result board 'fb' and return  true
    if find_empty(bo) == None:
        global fb
        fb = bo
        return True
    # First step: Find the coords of the first 'empty' location on the board using the find_empty func
    (i, j) = find_empty(bo)
    # Now, attempt to fill the empty space with a valid Sudoku value (1-9)
    for v in range(1,10):
        bo[i][j] = v
        # Check if the given number in the square validates the rules of Sudoku
        if (validate(bo, i, j) == True):
            # Now, recursively check if this current number can satisfy a potential solution
            # of the entire board by continuing to fill the rest of the squares.
            if (fill(bo)==True):
                return True
        # If the function hasnt returned by this point, it means there is no value (1-9) that can
        # satisfy the entire board, therefore we must backtrack to most previously filled square and
        # try a new value
        bo[i][j] = 0
    return False

# Checks to see if the new value at (i,j) is valid given the current board
def validate(bo, i, j):
    for k in range(len(bo)):
        # First check if the row and col that (i,j) occupies does not contain a duplicate
        if k != j and bo[i][k] == bo[i][j]:
            return False
        elif k != i and bo[k][j] == bo[i][j]:
            return False
    # Now, need to check the 3x3 grid that (i,j) falls in
    if j <= 2:
        index_j = 0
    elif j > 2 and j <= 5:
        index_j = 3
    else:
        index_j = 6

    if i <= 2:
        index_i = 0
    elif i > 2 and i <= 5:
        index_i = 3
    else:
        index_i = 6

    for p in range(index_i, index_i+3):
        for q in range(index_j, index_j+3):
            if (p != i and q != j and bo[p][q] == bo[i][j]):
                return False

    return True

# Locates the first occurance of a '0' in the board and returns its position
def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None

# Helper function that will print the entire board out neatly for testing purposes
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

# Helper function to determine if a mouse position falls within a coordinate range
def pointInRectangle(px, py, rw, rh, rx, ry):
    if px > rx and px < rx  + rw:
        if py > ry and py < ry + rh:
            return True
    return False

def main():
    # The default game board
    board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ] 

    # A backup of the board is kept for restting purposes
    board_backup = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ] 

    pygame.init()
    pygame.display.set_caption('SudokuSolver')

    # Creating the game window & background
    window_surface = pygame.display.set_mode((400, 550))
    background = pygame.Surface((400, 550))
    background.fill(pygame.Color('#000000'))

    # Creating the "Solve" button that allows the user to solve the board.
    button1 = SolveButton(
        "Solve",
        (280, 435),
        font=30,
        bg="white",
        feedback="Solved!")

    # This block of code is responsible for adding each Sudoku tile to an array called buttons.
    # The position of each tile is generated within the for loop, and then appended to the array
    buttons = []
    x = 6
    y = 6
    for i in range(9):
        for j in range(9):
            buttons.append(GridButton(board[i][j], (x,y), (i,j), background))
            if ((j+1)%3 == 0 and j != 0):
                x += 53
            else:
                x += 41      
        x = 6
        if ((i+1)%3 == 0 and i != 0):
             y += 53
        else:
             y += 41
    #--------------------------------------------------------------------------------------------    
    
    # This chunk of code is responsible for the message that will display if the current Sudoku board
    # does NOT have a solution. A message in the bottom left corner of the game board will appear, 
    # telling the user they must reset the game board.
    green = (0, 255, 0)
    blue = (0, 0, 128)
    errorFont = pygame.font.SysFont("comicsans", 18)
    errorTextTop = errorFont.render("This puzzle is not", True, green, blue)
    errorTextBottom = errorFont.render("solvable. Click Reset!", True, green, blue)
    textRectTop = errorTextTop.get_rect()
    textRectTop.center = (90, 450)
    textRectBottom = errorTextBottom.get_rect()
    textRectBottom.center = (90, 475)
    #-------------------------------------------------------------------------------------------------

    for b in buttons:
        b.render(window_surface)

    # Creating the pygame eventloop
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (button1.clicked(event) and button1.getText() != "Reset"):
                    fill(board)
                    if fb:
                        # If we got to here, it means the board DOES have a solution, so fill the board with the correct solution.
                        button1.setText("Solve")
                        button1.show(window_surface)
                        holder = []
                        for i in range(9):
                            for j in range(9):
                                holder.append(fb[i][j])
                        count = 0
                        for b in buttons:
                            b.setNumber(holder[count])
                            b.render(window_surface)
                            count += 1
                    else:
                        # Otherwise, the board doesn't have a solution, so display the error message.
                        window_surface.blit(errorTextTop, textRectTop)
                        window_surface.blit(errorTextBottom, textRectBottom)
                        button1.setText("Reset")
                        button1.show(window_surface)
                        pygame.display.flip()
                elif (button1.clicked(event) and button1.getText() == "Reset"):
                    button1.setText("Solve")
                    button1.show(window_surface)
                    holder = []
                    for i in range(9):
                        for j in range(9):
                            holder.append(board_backup[i][j])
                    count = 0
                    for b in buttons:
                        b.setNumber(holder[count])
                        b.render(window_surface)
                        count += 1
                    board = board_backup
                    pygame.draw.rect(window_surface, (0,0,0), pygame.Rect(0, 400, 200, 100))
                    pygame.display.flip()
                else:
                    for b in buttons:
                        b.render(window_surface)
                        if b.clicked(event, pygame.mouse.get_pos()):
                            # The following 2 lines are so the button will change color when clicked (to highlight it)
                            b.render(window_surface)
                            pygame.display.flip()
                            # If we got here, it means the user clicked on a board tile.
                            pygame.event.clear()
                            new_event = pygame.event.wait()
                            while (new_event.type != pygame.KEYDOWN):
                                new_event = pygame.event.wait()
                            if (new_event.key == pygame.K_0):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 0
                                b.setNumber(0)
                            elif (new_event.key == pygame.K_1):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 1
                                b.setNumber(1)
                            elif (new_event.key == pygame.K_2):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 2
                                b.setNumber(2)
                            elif (new_event.key == pygame.K_3):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 3
                                b.setNumber(3)
                            elif (new_event.key == pygame.K_4):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 4
                                b.setNumber(4)
                            elif (new_event.key == pygame.K_5):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 5
                                b.setNumber(5)
                            elif (new_event.key == pygame.K_6):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 6
                                b.setNumber(6)
                            elif (new_event.key == pygame.K_7):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 7
                                b.setNumber(7)
                            elif (new_event.key == pygame.K_8):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 8
                                b.setNumber(8)
                            elif (new_event.key == pygame.K_9):
                                coords = b.getPosInBoard()
                                board[coords[0]][coords[1]] = 9
                                b.setNumber(9)
                            b.render(window_surface)
                           
        button1.show(window_surface)
        pygame.display.update()

# The GridButton class represents every single Sudoku tile on the board. It is responsible for
# rendering the tiles on the display and getting data about each tile.
class GridButton:
    def __init__(self, text:str, position:tuple, posInBoard:tuple, background, size:tuple=(35,35)):
        self.posInBoard = posInBoard
        self.text = text
        self.position = position
        self.size = size
        self.button = pygame.Surface(size).convert()
        self.button.fill((255,255,255))

        font = pygame.font.SysFont("comicsans", 30)
        self.textSurf = font.render(f"{text}", True, (0,0,0))

    # Renders the individual tile onto the board
    def render(self, display:pygame.display):
        display.blit(self.button, self.position)
        display.blit(self.textSurf, self.position)

    # Sets a tile's number to a user-given input 1-9
    def setNumber(self, newNumber):
        self.text = newNumber
        font = pygame.font.SysFont("comicsans", 30)
        self.textSurf = font.render(f"{self.text}", True, (0,0,0))
        self.button.fill((255,255,255))

    # Returns a tuple representing the coordinates where this tile lies on the board
    def getPosInBoard(self):
        return self.posInBoard

    # Returns this tile's number
    def getNumber(self):
        return self.text

    # Checks to see if this tile was clicked by the user
    def clicked(self, events, coords:tuple):
        mousePos = coords
        if pointInRectangle(mousePos[0], mousePos[1], self.size[0], self.size[1], self.position[0], self.position[1]):
            if events.type == pygame.MOUSEBUTTONDOWN:
                self.button.fill((200,200,200))
                return True
        return False

class SolveButton:
    def __init__(self, text, pos, font, bg="white", feedback="", size:tuple=(100,50)):
        self.x, self.y = pos
        self.text = text
        self.font = pygame.font.SysFont("Comic Sans", font)
        self.size = size
        self.button = pygame.Surface(size).convert()
        self.button.fill((255,255,255))

        self.textSurf = self.font.render(f"{text}", True, (0,0,0))

    def show(self, display:pygame.display):
        display.blit(self.button, (self.x, self.y))
        display.blit(self.textSurf, (self.x, self.y))

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()
        if pointInRectangle(mousePos[0], mousePos[1], self.size[0], self.size[1], self.x, self.y):
            if events.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def getText(self):
        return self.text

    def setText(self, newText):
        self.text = newText
        self.textSurf = self.font.render(f"{self.text}", True, (0,0,0))

if __name__ == "__main__":
        main()