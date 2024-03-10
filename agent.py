import numpy as np

actions = [(-1, 0),  # Up
           (1, 0),  # Down
           (0, -1),  # Left
           (0, 1)]  # Right


class QLearningAgent:
    def __init__(self, maze, learning_rate=0.9, discount_factor=0.9, exploration_start=0.4, exploration_end=0.0001,
                 decay_rate=0.05, trained=False):

        self.maze = maze
        self.q_table = np.zeros((len(maze.grid), len(maze.grid[0]), 4))  # Q-table, initialized to 0s, first dimension
        # for the x-axis position in the maze, second for y-axis position, and third dimension for the possible actions
        self.learning_rate = learning_rate  # learning rate (alpha), how likely the agent will update the q-table
        self.discount_factor = discount_factor  # discount factor (gamma), importance of future reward in agent's decisions
        self.exploration_start = exploration_start  # max exploration value (max epsilon)
        self.exploration_end = exploration_end  # min exploration value (min epsilon)
        self.decay_rate = decay_rate  # epsilon decay in training
        self.trained = trained

    def get_exploration_rate(self, current_episode):
        exploration_rate = self.exploration_start * (self.exploration_end / self.exploration_start) ** (
                current_episode * self.decay_rate)
        return exploration_rate

    def get_action(self, state, current_episode):
        if self.trained:  # if the agent is already trained he will 100% trust his q-table
            exploration_rate = 0
        else:
            exploration_rate = self.get_exploration_rate(current_episode)  # during training, he will calculate epsilon

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
