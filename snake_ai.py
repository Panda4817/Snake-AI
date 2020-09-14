import tempfile
import os

import numpy as np
import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import dynamic_step_driver
from tf_agents.environments import utils
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import q_network
from tf_agents.policies import policy_saver
from tf_agents.policies import py_tf_eager_policy
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

from snake import *

tf.compat.v1.enable_v2_behavior()

tempdir = os.getenv("TEST_TMPDIR", tempfile.gettempdir())

collect_steps_per_iteration = 1000
replay_buffer_capacity = 100000

fc_layer_params = (100,)

batch_size = 100
learning_rate = 1e-3
log_interval = 5

num_eval_episodes = 10
eval_interval = 1000

# Initialise board width, height and tile size
width, height = 600, 400
tile_size = 10
leftover = 20
h = int(height / tile_size)
w = int((width - (leftover * tile_size)) / tile_size)

# Initialise AI board and snake
boardAi = Board(h=h, w=w)
snakeAi = Snake()
snakeAi.reset(boardAi)

environment = SnakeAiEnvironment(snakeAi, boardAi)
# print("validating")
# utils.validate_py_environment(environment, episodes=1)
train_env = tf_py_environment.TFPyEnvironment(environment)
eval_env = tf_py_environment.TFPyEnvironment(environment)

print("creating network")
q_net = q_network.QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params=fc_layer_params)

optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

global_step = tf.compat.v1.train.get_or_create_global_step()

print("creating agent")
agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=global_step)
agent.initialize()

print("setting up buffer")
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity)

collect_driver = dynamic_step_driver.DynamicStepDriver(
    train_env,
    agent.collect_policy,
    observers=[replay_buffer.add_batch],
    num_steps=collect_steps_per_iteration)

# Initial data collection
print("collecting initial data")
collect_driver.run()

# Dataset generates trajectories with shape [BxTx...] where
# T = n_step_update + 1.
print("dataset generates trajectories")
dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, sample_batch_size=batch_size,
    num_steps=2).prefetch(3)

iterator = iter(dataset)

# (Optional) Optimize by wrapping some of the code in a graph using TF function.
agent.train = common.function(agent.train)

def train_one_iteration():

    # Collect a few steps using collect_policy and save to the replay buffer.
    collect_driver.run()

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience)

    iteration = agent.train_step_counter.numpy()
    print ('iteration: {0} loss: {1}'.format(iteration, train_loss.loss))

print("setting up checkpoint and policy saver")
checkpoint_dir = os.path.join(tempdir, 'checkpoint5')
train_checkpointer = common.Checkpointer(
    ckpt_dir=checkpoint_dir,
    max_to_keep=1,
    agent=agent,
    policy=agent.policy,
    replay_buffer=replay_buffer,
    global_step=global_step
)

policy_dir = os.path.join(tempdir, 'policy')
tf_policy_saver = policy_saver.PolicySaver(agent.policy)

for i in range(10):
    print('Training one iteration....')
    train_one_iteration()

train_checkpointer.save(global_step)

train_checkpointer.initialize_or_restore()
global_step = tf.compat.v1.train.get_global_step()

tf_policy_saver.save(policy_dir)

saved_policy = tf.compat.v2.saved_model.load(policy_dir)