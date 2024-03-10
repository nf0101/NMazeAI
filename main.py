import concurrent
from concurrent import futures
import sys
import threading
import time

import numpy as np
import pygame

from mazelib import Maze
from mazelib.generate.CellularAutomaton import CellularAutomaton
from mazelib.generate.Division import Division
from mazelib.generate.DungeonRooms import DungeonRooms
from mazelib.generate.HuntAndKill import HuntAndKill
from mazelib.generate.MazeGenAlgo import MazeGenAlgo
from mazelib.generate.Prims import Prims
from mazelib.generate.Sidewinder import Sidewinder
from mazelib.generate.TrivialMaze import TrivialMaze
from mazelib.generate.Wilsons import Wilsons
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from mazelib.solve.RandomMouse import RandomMouse
from mazelib.solve.ShortestPath import ShortestPath

from agent import QLearningAgent
from learning import test_agent, train_agent
from search import bfs, dfs

steps = []
time_elapsed = []
dim_cell = 18
rows = 22
cols = 39

m = Maze()
m.generator = Prims(rows, cols)
m.generate()
m.generate_entrances()
m.grid[m.start[0]][m.start[1]] = 0
m.grid[m.end[0]][m.end[1]] = 0
print(m.start, m.end)
start = time.time()
bfs(m)
end = time.time()
print(f"Elapsed time bfs: {end - start}")
start = time.time()
dfs(m)
end = time.time()
print(f"Elapsed time dfs: {end - start}")
np.savetxt("maze.txt", m.grid)
width, height = len(m.grid[0]) * dim_cell, len(m.grid) * dim_cell
m.solver = BacktrackingSolver()
start = time.time()
m.solve()
end = time.time()
print(f"Elapsed time ShortestPath: {end - start}")
print(f"Soluzioni: {len(m.solutions[0])}")

def start_agent():
    print("Start agent")
    for i in range(1):

        print(i)
        # np.savetxt("maze.txt", arr_reshaped)  # code to save the maze

        agent = QLearningAgent(m)
        # code to save the qtable
        # arr_reshaped = agent.q_table.reshape(agent.q_table.shape[0], -1)
        # np.savetxt("qtable.txt", arr_reshaped)
        # loaded_arr = np.loadtxt("qtable.txt")

        # loaded_qtable = loaded_arr.reshape(
        #     loaded_arr.shape[0], loaded_arr.shape[1] // agent.q_table.shape[2], agent.q_table.shape[2])
        # agent.q_table = load_original_arr
        start = time.time()
        train_agent(agent, m, num_episodes=200)
        agent.trained = True

        a = test_agent(agent, m)
        end = time.time()
        # code to update the saved qtable
        # arr_reshaped = agent.q_table.reshape(agent.q_table.shape[0], -1)
        # np.savetxt("qtable.txt", arr_reshaped)
        steps.append(a[0])

        print(f"Elapsed time agent: {end - start}")
        time_elapsed.append(end - start)
    print(f"Average time: {sum(time_elapsed) / len(time_elapsed)}")
    print(f"Average steps: {sum(steps) / len(steps)}")

    for pos in a[2]:
        m.grid[pos[0]][pos[1]] = 3


def main():
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("NMazeAI")
    pygame.init()
    start_agent()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill((255, 255, 255))  # White for empty cells
        for i in range(len(m.grid)):
            for j in range(len(m.grid[0])):
                color = (255, 255, 255)

                if (i, j) == m.start:
                    color = (255, 0, 0)  # Red for start
                elif (i, j) == m.end:
                    color = (0, 255, 0)  # Green for end
                elif m.grid[i][j] == 1:
                    color = (0, 0, 0)  # Black for walls
                elif m.grid[i][j] == 3:
                    color = (0, 0, 255)  # Blue for solution
                pygame.draw.rect(window, color, pygame.Rect(j * dim_cell, i * dim_cell, dim_cell, dim_cell))
        pygame.display.flip()


if __name__ == "__main__":
    main()
    print("Done!")


