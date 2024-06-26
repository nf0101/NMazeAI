import matplotlib
from agent import actions
import matplotlib.pyplot as plt

# matplotlib.use('Agg')
# matplotlib.use('Agg')
# plt.ioff()

goal_reward = 5000
wall_penalty = -100
step_penalty = -15


def finish_episode(agent, maze, current_episode, train=True):
    current_state = maze.start
    is_done = False
    episode_reward = 0
    episode_step = 0
    path = [current_state]
    while not is_done:
        action = agent.get_action(current_state, current_episode)
        next_state = (current_state[0] + actions[action][0], current_state[1] + actions[action][1])  # calculate next_state

        # Check if next_state is a wall or out of bounds
        if (next_state[0] < 0 or next_state[0] >= len(maze.grid) or next_state[1] < 0
                or next_state[1] >= len(maze.grid[0]) or maze.grid[next_state[0]][next_state[1]] == 1):
            reward = wall_penalty
            next_state = current_state

        # Maze solved
        elif next_state == maze.end:
            print("Maze solved!")
            path.append(current_state)
            reward = goal_reward
            is_done = True

        else:  # Made step without finding solution
            reward = step_penalty
            if current_state != maze.start:
                path.append(current_state)

        episode_reward += reward
        if current_state != maze.start:
            episode_step += 1

        if train:  # if training, update q-table
            agent.update_q_table(current_state, action, next_state, reward)

        current_state = next_state  # go on next_state
    print(current_episode, episode_step)

    return episode_reward, episode_step, path


def test_agent(agent, maze, num_episodes=1):
    print("Start test")
    episode_reward, episode_step, path = finish_episode(agent, maze, num_episodes, train=False)

    print("Learned Path:")
    for row, col in path:
        print(f"({row}, {col})-> ", end='')
    print("Goal!")

    print("Number of steps:", episode_step)
    print("Total reward:", episode_reward)

    return episode_step, episode_reward, path


def train_agent(agent, maze, num_episodes=100):
    episode_rewards = []
    episode_steps = []

    for episode in range(num_episodes):
        episode_reward, episode_step, path = finish_episode(agent, maze, episode, train=True)
        episode_rewards.append(episode_reward)
        episode_steps.append(episode_step)

    # Plotting the data after training is completed
    # plt.figure(figsize=(10, 5))
    #
    # plt.subplot(1, 2, 1)
    # plt.plot(episode_rewards)
    # plt.xlabel('Episode')
    # plt.ylabel('Cumulative Reward')
    # plt.title('Reward per Episode')
    #
    # average_reward = sum(episode_rewards) / len(episode_rewards)
    # print(f"The average reward is: {average_reward}")
    #
    # plt.subplot(1, 2, 2)
    # plt.plot(episode_steps)
    # plt.xlabel('Episode')
    # plt.ylabel('Steps Taken')
    # plt.ylim(0, 100000)
    # plt.title('Steps per Episode')
    #
    # average_steps = sum(episode_steps) / len(episode_steps)
    # print(f"The average steps is: {average_steps}")
    #
    # plt.tight_layout()
    # plt.savefig(f"image{time.time()}.png")