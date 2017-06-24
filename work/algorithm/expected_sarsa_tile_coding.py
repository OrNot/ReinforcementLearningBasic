import sys
import itertools


sys.path.append('/home/ornot/GymRL')
from lib import utility


def expected_sarsa(env, estimator, num_episodes, statistics, discount_factor=1.0, epsilon=0.1, epsilon_decay=1.0):
    """
    expected sarsa algorithm for on-policy TD control using Function Approximation.
    Args:
        env: OpenAI environment.
        estimator: Action-Value function estimator
        num_episodes: Number of episodes to run for.
        statistics:An EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
        discount_factor: Lambda time discount factor.
        epsilon: Chance the sample a random action. Float betwen 0 and 1.
        epsilon_decay: Each episode, epsilon is decayed by this factor

    Returns:

    """

    for i_episode in range(num_episodes):
        # The policy we're following
        e_greedy_policy = utility.make_epsilon_greedy_policy_with_fa(
            estimator, epsilon * epsilon_decay**i_episode, env.action_space.n)

        # Print out which episode we're on, useful for debugging.
        # Also print reward for last episode
        last_reward = statistics.episode_rewards[i_episode - 1]
        sys.stdout.flush()

        # Reset the environment and pick the first action
        obvservation = env.reset()

        for t in itertools.count():
            action = utility.make_decision(e_greedy_policy, obvservation)
            next_observation, reward, done, _ = env.step(action)

            # Update statistics
            statistics.episode_rewards[i_episode] += reward
            statistics.episode_lengths[i_episode] = t

            expected_next_q = 0
            next_actions = e_greedy_policy(next_observation)
            for action_index, action_prob in enumerate(next_actions):
                expected_next_q += action_prob * \
                    estimator.predict(next_observation, action_index)

            td_target = reward + discount_factor * expected_next_q

            # Update the function approximator using our target
            estimator.update(obvservation, action, td_target)

            print("\rStep {} @ Episode {}/{} ({})".format(t,
                                                          i_episode + 1, num_episodes, last_reward), end="")

            if done:
                break

            obvservation = next_observation
