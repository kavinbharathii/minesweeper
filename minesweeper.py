# minesweeper in python using pygame
# I am using bees in honor of Daniel Shiffman and Bees And Bombs , instead of the traditional mines...


from time import sleep
from matplotlib.pyplot import flag
import pygame
import random

pygame.font.init()

font = pygame.font.Font('freesansbold.ttf', 16)

numbees = 10
width = 400
height = 400
rez = 20

display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Minesweeper')

class Cell:
    def __init__(self, x, y, value):
        self.val = value
        self.revealed = False
        self.flagged = False
        self.x = x
        self.y = y

    def reveal(self):
        self.revealed = True

    def flag(self):
        self.revealed = False
        self.flagged = True

    def draw(self, win):
        if self.revealed:
            if self.val == -1:
                pygame.draw.rect(win, (190, 190, 190), (self.x * rez, self.y * rez, rez, rez))
                pygame.draw.circle(win, (51, 51, 51), ((self.x * rez) + rez // 2, (self.y * rez) + rez // 2), rez // 4)
            else:
                text = font.render(str(self.val), True, (169, 169, 169))
                win.blit(text, (((self.x * rez) + rez // 2) - 4, ((self.y * rez) + rez // 2) - 6))
        elif self.flagged:
            text = font.render('F', True, (169, 169, 169))
            win.blit(text, (((self.x * rez) + rez // 2) - 4, ((self.y * rez) + rez // 2) - 6))

grid = [[Cell(i, j, 0) for j in range(height // rez)] for i in range(width // rez)]
bees = []

for _ in range(numbees):
    i = random.randint(0, (width // rez) - 1)
    j = random.randint(0, (height // rez) - 1)
    grid[i][j].val = -1
    bees.append([i, j])

# neighbour checking algorithm...
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j].val == -1:
            pass
        else:
            total = 0
            for n in range(-1, 2):
                for m in range(-1, 2):
                    if (-1 < i + n < len(grid) and -1 < j + m < len(grid[0])): 
                        if grid[i + n][j + m].val == -1:
                            total += 1

            grid[i][j].val = total

def get_mouse_pos():
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    return (x - (x % rez), y - (y % rez))

def draw_grid():
    for i in range(1, width // rez):
        pygame.draw.line(display, (169,  169, 169), (0, i * rez), (width, i * rez))

    for j in range(1, height // rez):
        pygame.draw.line(display, (169,  169, 169), (j * rez, 0), (j * rez, height))

    for row in grid:
        for cell in row:
            cell.draw(display)

def cascade(grid_obj):
    for row in grid_obj:
        for cell in row:
            cell.reveal()

def floodfill(pos, count = 0):
    x, y = pos
    if grid[x][y].val > 2 or grid[x][y].val < 0:
        return
    if count > 5:
        return
    else:
        if not grid[x][y].flagged:
            grid[x][y].reveal()
        if y > -1:
            floodfill((x, y - 1), count + 1)
        
        if x < width // rez - 1:
            floodfill((x + 1, y), count + 1)
        
        if y < height // rez - 1:
            floodfill((x, y + 1), count + 1)

        if x > -1:
            floodfill((x - 1, y), count + 1)

def main():
    run = True
    flag_counter = 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = get_mouse_pos()
                grid_x, grid_y = mouse_x // rez, mouse_y // rez
                if event.button == 3:
                    if flag_counter > len(bees):
                        cascade()
                    grid[grid_x][grid_y].flag()
                    flag_counter += 1
                else:
                    if [grid_x, grid_y] in bees:
                        cascade(grid)  
                        draw_grid()
                        pygame.display.flip()  
                        sleep(2)
                        run = False

                    elif grid[grid_x][grid_y].val == 0:
                        floodfill((grid_x, grid_y))

                    else:
                        grid[grid_x][grid_y].reveal()

        draw_grid()
        pygame.display.flip()

main()
