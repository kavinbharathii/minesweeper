# minesweeper in python using pygame


import pygame
import random
import numpy

pygame.font.init()

font = pygame.font.Font('freesansbold.ttf', 16)

numbees = 10
width = 400
height = 400
rez = 40


display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Minesweeper')

grid = numpy.empty(shape = (width // rez, height // rez))
# grid = []
bees = []

# using '_' because I have no need to save the info in a variable
for _ in range(numbees + 1):
    i = random.randint(0, (width // rez) - 1)
    j = random.randint(0, (height // rez) - 1)
    grid[i][j] = -1
    bees.append([i, j])


for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == -1:
            pass
        else:
            total = 0
            for n in range(-1, 2):
                for m in range(-1, 2):
                    if (-1 < i + n < len(grid) and -1 < j + m < len(grid[0])): 
                        if grid[i + n][j + m] == -1:
                            total += 1
                        else:
                            pass

            grid[i][j] = total

def get_mouse_pos():
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]
    return (x - (x % rez), y - (y % rez))


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if [get_mouse_pos()[0] // rez, get_mouse_pos()[1] // rez] in bees:
                    pygame.draw.circle(display, (169, 169, 169), (get_mouse_pos()[0] + rez // 2, get_mouse_pos()[1] + rez // 2), rez // 4)
                else:
                    text = font.render(str(grid[get_mouse_pos()[0] // rez][get_mouse_pos()[1] // rez]).replace('.0', ''), True, (255, 255, 255))
                    display.blit(text, ((get_mouse_pos()[0] + rez // 2) - 4, (get_mouse_pos()[1] + rez // 2) - 6))

        for i in range(1, width // rez):
            pygame.draw.line(display, (169,  169, 169), (0, i * rez), (width, i * rez))

        for j in range(1, height // rez):
            pygame.draw.line(display, (169,  169, 169), (j * rez, 0), (j * rez, height))


        pygame.display.flip()


main()
