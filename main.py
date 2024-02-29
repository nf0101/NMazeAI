import sys

import pygame

from mazelib import Maze
from mazelib.generate.Prims import Prims
# import matplotlib.pyplot as plt

rows = 27
cols = 34
m = Maze()
m.generator = Prims(rows, cols)
m.generate()
m.generate_entrances()
print(m.grid)

print(m.tostring(True, False))
# test
# Dimensioni di ogni cella (in pixel)
dim_cell = 18
larghezza, altezza = len(m.grid[0]) * dim_cell, len(m.grid) * dim_cell
schermo = pygame.display.set_mode((larghezza, altezza))
pygame.display.set_caption("Labirinto Q-Learning")
pygame.init()

# Disegno del labirinto
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    schermo.fill((255, 255, 255))
    for i in range(len(m.grid)):
        for j in range(len(m.grid[0])):
            spessore = dim_cell
            colore = (255, 255, 255)  # Bianco per le celle vuote
            if m.grid[i][j] == 1:
                if (i, j) == m.start:
                    colore = (0, 255, 0)
                elif (i, j) == m.end:
                    colore = (255, 0, 0)
                else:
                    colore = (0, 0, 0)  # Nero per i muri
            pygame.draw.rect(schermo, colore, pygame.Rect(j * dim_cell, i * dim_cell, dim_cell,
                                                          dim_cell))
    pygame.display.flip()
