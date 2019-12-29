import numpy as np
import gym
import gym_tetris

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input
from keras.optimizers import Adam
from keras.layers.core import Reshape

from rl.agents.cem import CEMAgent
from rl.memory import EpisodeParameterMemory

ENV_NAME = 'Tetris-v1'


# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

nb_actions = env.action_space.nvec
obs_dim = env.observation_space.shape[0]

inp = Input((1, 20, 10))
x = Dense(200,activation='sigmoid')(inp)
x = Dense(1800,activation='softplus')(x)
x = Dense(1800,activation='softplus')(x)
x = Dense(1800,activation='softplus')(x)
x = Dense(600,activation='softplus')(x)
x = Dense(200,activation='softplus')(x)
x = Flatten()(x)
y = Dense(8, activation = 'softmax')(x)
model = Model(inp,y)

print(model.summary())


# Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
# even the metrics!
memory = EpisodeParameterMemory(limit=250, window_length=1)

cem = CEMAgent(model=model, nb_actions=nb_actions, memory=memory,
               batch_size=50, nb_steps_warmup=2000, train_interval=50, elite_frac=0.05)
cem.compile()

# Okay, now it's time to learn something! We visualize the training here for show, but this
# slows down training quite a lot. You can always safely abort the training prematurely using
# Ctrl + C.
cem.fit(env, nb_steps=100000, visualize=False, verbose=2)

# After training is done, we save the best weights.
cem.save_weights('cem_{}_params.h5f'.format(ENV_NAME), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
cem.test(env, nb_episodes=5, visualize=True)