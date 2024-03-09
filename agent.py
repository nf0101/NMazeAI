import numpy as np

actions = [(-1, 0),  # Up
           (1, 0),  # Down
           (0, -1),  # Left
           (0, 1)]  # Right


class QLearningAgent:
    def __init__(self, maze, learning_rate=0.9, discount_factor=0.9, exploration_start=0.9, exploration_end=0.001,
                 num_episodes=100):

        self.maze = maze
        self.q_table = np.zeros((len(maze.grid), len(maze.grid[0]), 4))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_start = exploration_start
        self.exploration_end = exploration_end
        self.num_episodes = num_episodes

    def get_exploration_rate(self, current_episode):
        exploration_rate = self.exploration_start * (self.exploration_end / self.exploration_start) ** (
                current_episode / self.num_episodes)
        return exploration_rate

    def get_action(self, state, current_episode):
        exploration_rate = self.get_exploration_rate(current_episode)
        # exploration_rate = 0
        if np.random.rand() < exploration_rate:  # random choose between actions
            return np.random.randint(4)

        else:
            return np.argmax(self.q_table[state])  # choose the action with highest q-value in state

    def update_q_table(self, state, action, next_state, reward):
        best_next_action = np.argmax(self.q_table[next_state])

        current_q_value = self.q_table[state][action]

        new_q_value = current_q_value + self.learning_rate * (
                reward + self.discount_factor * self.q_table[next_state][best_next_action] - current_q_value)

        self.q_table[state][action] = new_q_value
