import torch
from unityagents import UnityEnvironment
import numpy as np
from ddpg_agent import Agent
from collections import deque
import matplotlib.pyplot as plt

seed=10

# select this option to load version 1 (with a single agent) of the environment
env = UnityEnvironment(file_name='Reacher', seed=seed,worker_id=1)


# get the default brain
brain_name = env.brain_names[0]
brain = env.brains[brain_name]


# reset the environment
env_info = env.reset(train_mode=True)[brain_name]

# number of agents
num_agents = len(env_info.agents)
print('Number of agents:', num_agents)

# size of each action
action_size = brain.vector_action_space_size
print('Size of each action:', action_size)

# examine the state space 
states = env_info.vector_observations
state_size = states.shape[1]
print('There are {} agents. Each observes a state with length: {}'.format(states.shape[0], state_size))
print('The state for the first agent looks like:', states[0])

agent = Agent(state_size, action_size, seed)

agent.actor_local.state_dict(torch.load('actor.pth'))
agent.actor_local.state_dict(torch.load('critic.pth'))
print_every = 10
save_every = 100


def train(n_episodes=1000, max_t=1000, eps_start=1.0, eps_end=0.1, eps_decay=0.0001):
    """Deep Q-Learning.
    
    Params
    ======
        n_episodes (int): maximum number of training episodes
        max_t (int): maximum number of timesteps per episode
        eps_start (float): starting value of epsilon, for epsilon-greedy action selection
        eps_end (float): minimum value of epsilon
        eps_decay (float): multiplicative factor (per episode) for decreasing epsilon
    """
    total_scores = []      # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores

    eps = eps_start                    # initialize epsilon
    for i_episode in range(1, n_episodes+1):
        env_info = env.reset(train_mode=True)[brain_name] # reset the environment
        state = env_info.vector_observations          # get the current state
        agent.reset()
        scores = np.zeros(num_agents)
        for t in range(max_t):
            action = agent.act(eps, state)
            env_info = env.step(action)[brain_name]        # send the action to the environment
            next_state = env_info.vector_observations
            reward = env_info.rewards
            done = env_info.local_done
            scores += reward

            agent.step(t, state, action, reward, next_state, done)
            state = next_state

            if np.any(done):
                break
        scores_window.append(scores)
        total_scores.append(scores)
        total_average_score = np.mean(scores_window)
        eps = max(eps_end, eps-eps_decay) # decrease epsilon
        if i_episode % print_every == 0:
            print('\rEpisode {}\tTotal Average Score: {:.2f}'.
                  format(i_episode, total_average_score))

        if i_episode % save_every == 0:
            torch.save(agent.actor_local.state_dict(), 'actor.pth')
            torch.save(agent.critic_local.state_dict(), 'critic.pth')
        if np.mean(scores_window) >= 30.0:
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'
                  .format(i_episode-100, total_average_score))
            torch.save(agent.actor_local.state_dict(), 'actor.pth')
            torch.save(agent.critic_local.state_dict(), 'critic.pth')
            break

    return total_scores


scores = train()


# plot the scores
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.arange(len(scores)), scores)
plt.ylabel('Score')

plt.xlabel('Episode #')
plt.show()


# In[ ]:


env.close()


# ### 4. It's Your Turn!
# 
# Now it's your turn to train your own agent to solve the environment!  A few **important notes**:
# - When training the environment, set `train_mode=True`, so that the line for resetting the environment looks like the following:
# ```python
# env_info = env.reset(train_mode=True)[brain_name]
# ```
# - To structure your work, you're welcome to work directly in this Jupyter notebook, or you might like to start over with a new file!  You can see the list of files in the workspace by clicking on **_Jupyter_** in the top left corner of the notebook.
# - In this coding environment, you will not be able to watch the agents while they are training.  However, **_after training the agents_**, you can download the saved model weights to watch the agents on your own machine! 

# In[ ]:





# In[ ]:





# In[ ]:




