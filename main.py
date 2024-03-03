import sys

import numpy as np
import pygame

from mazelib import Maze
from mazelib.generate.Prims import Prims

from agent import QLearningAgent
from learning import test_agent, train_agent, finish_episode

# import matplotlib.pyplot as plt
# for i in range(1):
# print(i)
rows = 15
cols = 20
m = Maze()
m.generator = Prims(rows, cols)
m.generate()
m.generate_entrances()
m.grid[m.start[0]][m.start[1]] = 0
m.grid[m.end[0]][m.end[1]] = 0

# test
# Dimensioni di ogni cella (in pixel)
# dim_cell = 18
# larghezza, altezza = len(m.grid[0]) * dim_cell, len(m.grid) * dim_cell
# schermo = pygame.display.set_mode((larghezza, altezza))
# pygame.display.set_caption("Labirinto Q-Learning")
# pygame.init()

agent = QLearningAgent(m)

loaded_arr = np.loadtxt("qtable.txt")

load_original_arr = loaded_arr.reshape(
    loaded_arr.shape[0], loaded_arr.shape[1] // agent.q_table.shape[2], agent.q_table.shape[2])

agent.q_table = load_original_arr
train_agent(agent, m, num_episodes=5000)
# test_agent(agent, m)
arr_reshaped = agent.q_table.reshape(agent.q_table.shape[0], -1)
np.savetxt("qtable.txt", arr_reshaped)
#
# # saving reshaped array to file.

# episode_rewards = []
# episode_steps = []
# for episode in range(50000):
#     episode_reward, episode_step = test_agent(agent, m)
#
#     # Store the episode's cumulative reward and the number of steps taken in their respective lists
#     episode_rewards.append(episode_reward)
#     episode_steps.append(episode_step)
#
# average_reward = sum(episode_rewards) / len(episode_rewards)
# print(f"The average reward is: {average_reward}")
#
# average_steps = sum(episode_steps) / len(episode_steps)
# print(f"The average steps is: {average_steps}")
#
# print((load_original_arr == agent.q_table).all())

# print(test_agent(agent, m))

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     schermo.fill((255, 255, 255))
#     for i in range(len(m.grid)):
#         for j in range(len(m.grid[0])):
#             spessore = dim_cell
#             colore = (255, 255, 255)  # Bianco per le celle vuote
#
#             if (i, j) == m.start:
#                     colore = (0, 255, 0)
#             elif (i, j) == m.end:
#                     colore = (255, 0, 0)
#             elif m.grid[i][j] == 1:
#                 colore = (0, 0, 0)  # Nero per i muri
#             pygame.draw.rect(schermo, colore, pygame.Rect(j * dim_cell, i * dim_cell, dim_cell,
#                                                           dim_cell))
#     pygame.display.flip()
    # x = -1
    # while x != 9:
    #     print("AAA")
    #     x = int(input())
    #     if x == 0:
    #         test_agent(agent, m)
    #     elif x == 1:
    #         train_agent(agent, m, num_episodes=1000000)
    #     elif x == 9:
    #         sys.exit()



