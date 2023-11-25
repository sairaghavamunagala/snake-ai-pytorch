import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.num_episode=0
        self.epsilon=0 # to control randomness
        self.gamma=0 #discount rate
        self.memory=deque(MAX_MEMORY) #if memory exceeds it will remove element from first


    def get_state(self, game):
        pass

       
    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass
      

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

def train():
    """
    This will get old state of game,
    based on the state it will give action,
    it will get next state,
    it will train the using short memory and remember it,
    if gameover,it will reset game and do long term training,
    if score greater than record ,then it will update
    and save the model.
    """
    plot_scores = list()
    plot_mean_scores = list()
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.num_episode += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

           


if __name__ == '__main__':
    train()