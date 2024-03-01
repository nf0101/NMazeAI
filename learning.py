from agent import actions
import matplotlib.pyplot as plt

goal_reward = 100
wall_penalty = -10
step_penalty = -1


def finish_episode(agent, maze, current_episode, train=True):

    current_state = maze.start

    is_done = False
    episode_reward = 0
    episode_step = 0
    path = [current_state]

    while not is_done:

        action = agent.get_action(current_state, current_episode)
        next_state = (current_state[0] + actions[action][0], current_state[1] + actions[action][1])

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

        # Made step without finding solution
        else:
            path.append(current_state)
            reward = step_penalty

        episode_reward += reward
        episode_step += 1

        if train:
            agent.update_q_table(current_state, action, next_state, reward)

        current_state = next_state

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

    return episode_step, episode_reward


def train_agent(agent, maze, num_episodes=100):
    # Lists to store the data for plotting
    episode_rewards = []
    episode_steps = []

    # Loop over the specified number of episodes
    for episode in range(num_episodes):
        episode_reward, episode_step, path = finish_episode(agent, maze, episode, train=True)

        # Store the episode's cumulative reward and the number of steps taken in their respective lists
        episode_rewards.append(episode_reward)
        episode_steps.append(episode_step)

    # Plotting the data after training is completed
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(episode_rewards)
    plt.xlabel('Episode')
    plt.ylabel('Cumulative Reward')
    plt.title('Reward per Episode')

    average_reward = sum(episode_rewards) / len(episode_rewards)
    print(f"The average reward is: {average_reward}")

    plt.subplot(1, 2, 2)
    plt.plot(episode_steps)
    plt.xlabel('Episode')
    plt.ylabel('Steps Taken')
    plt.ylim(0, 100)
    plt.title('Steps per Episode')

    average_steps = sum(episode_steps) / len(episode_steps)
    print(f"The average steps is: {average_steps}")

    plt.tight_layout()
    plt.show()
