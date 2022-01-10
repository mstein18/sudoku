# This is a simple python program that will solve a given Sudoku board using a backtracking algorithm.
# In addition, a GUI is provided, its purpose is to represent the Sudoku board and allow the user to
# press a "solve" button to see the before and after.
# *CITATION* The template of the GUI code was provided in an online tutorial. The Grid class,
# the Cube class, and the redraw function were written by TechWithTim. This code can be found
# here: https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/. All
# other functions classes were written by myself, Mark Steinbruck. More information is provided in the README.md file.

import winsound
import pygame
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

# Helper function that will print the entire board out neatly
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

class Grid:

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

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

class Button:
    def __init__(self, text, pos, font, bg="black", feedback=""):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Comic Sans", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("Black"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(button1.surface, (self.x, self.y))

    def click(self, event, board):
        fill(board.board)
        board.board = fb
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="white")

def redraw(window, board):
    window.fill((255,255,255))
    fnt = pygame.font.SysFont("comicsans", 40)
    button1.show(window)
    board.draw(window)

def main():
    screen = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9,9,540,540)
    isrunning = True
    key = None
    strikes = 0
    start = time.time()
    while isrunning:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isrunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                (x,y) = pos
                if (x > 215 and x < 290 and y > 555 and y < 590):
                    button1.click(event, board)
                    board = Grid(9,9,540,540)
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        if board.selected and key != None:
            board.sketch(key)
        redraw(screen,board)
        pygame.display.update()

button1 = Button(
    "Solve",
    (215, 550),
    font=30,
    bg="white",
    feedback="Solved!")

main()
pygame.quit()