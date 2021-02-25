import tensorflow as tf
import os

import rlcard
from rlcard.agents import NFSPAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger
from datetime import datetime

# Make environment
env = rlcard.make('no-limit-holdem', config={'seed': 0, 'game_player_num': 5, 'chips_for_each': [100]*5})
eval_env = rlcard.make('no-limit-holdem', config={'seed': 0, 'game_player_num': 5, 'chips_for_each': [100]*5})

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 10000
evaluate_num = 1000
episode_num = 1000000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 64

# The paths for saving the logs and learning curves
log_dir = './experiments/nolimit_holdem_nfsp_result/'

# The paths for saving the model
model_dir = 'models/nolimit_holdem_nfsp'

# Set a global seed
set_global_seed(0)
check_point_path = os.path.join('models/nolimit_holdem_nfsp')

with tf.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents = []
    for i in range(env.player_num):
        agent = NFSPAgent(sess,
                          scope='nfsp' + str(i),
                          action_num=env.action_num,
                          state_shape=env.state_shape,
                          hidden_layers_sizes=[512, 512],
                          anticipatory_param=0.1,
                          min_buffer_size_to_learn=memory_init_size,
                          q_replay_memory_init_size=memory_init_size,
                          train_every=train_every,
                          q_train_every=train_every,
                          q_mlp_layers=[512, 512])
        agents.append(agent)

    random_agents = []
    for i in range(env.player_num - 1):
        random_agent = RandomAgent(action_num=eval_env.action_num)
        random_agents.append(random_agent)

    # random_agent = RandomAgent(action_num=eval_env.action_num)
    env.set_agents(agents)
    eval_env.set_agents([agents[0], random_agents[0], random_agents[1], random_agents[2], random_agents[3]])
    #     eval_env.set_agents([agents[0], random_agents[0]])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()
    saver.restore(sess, tf.train.latest_checkpoint(check_point_path))

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):
        if episode % 10000 == 0:
            print('\nepisode = ', episode, ' ', datetime.now())
        # First sample a policy for the episode
        for agent in agents:
            agent.sample_episode_policy()

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for i in range(env.player_num):
            for ts in trajectories[i]:
                agents[i].feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('NFSP')

    # Save model
    # save_dir = 'models/nolimit_holdem_nfsp'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(model_dir, 'model'))