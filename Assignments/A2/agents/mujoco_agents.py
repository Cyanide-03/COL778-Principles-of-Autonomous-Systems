import itertools
import torch
from torch import nn
import random
from torch import optim
import numpy as np
from tqdm import tqdm
import torch.distributions as distributions

import os
import numpy as np
from utils.replay_buffer import ReplayBuffer
from agents.base_agent import BaseAgent
import utils.pytorch_util as ptu
from policies.experts import load_expert_policy
# import utils.utils as utils
from utils.utils import *


class ImitationAgent(BaseAgent):
    '''
    Please implement an Imitation Learning agent. Read train_agent.py to see how the class is used. 
    
    
    Note: 1) You may explore the files in utils to see what helper functions are available for you.
          2)You can add extra functions or modify existing functions. Dont modify the function signature of __init__ and train_iteration.  
          3) The hyperparameters dictionary contains all the parameters you have set for your agent. You can find the details of parameters in config.py.  
          4) You may use the util functions like utils/pytorch_util/build_mlp to construct your NN. You are also free to write a NN of your own. 
    
    Usage of Expert policy:
        Use self.expert_policy.get_action(observation:torch.Tensor) to get expert action for any given observation. 
        Expert policy expects a CPU tensors. If your input observations are in GPU, then 
        You can explore policies/experts.py to see how this function is implemented.
    '''

    def __init__(self, observation_dim, action_dim, args=None, discrete=False, **hyperparameters):
        super().__init__()
        self.hyperparameters = hyperparameters
        self.action_dim  = action_dim
        self.observation_dim = observation_dim
        self.is_action_discrete = discrete
        self.args = args
        self.replay_buffer = ReplayBuffer(5000) #you can set the max size of replay buffer if you want
        

        # initialize your model and optimizer and other variables you may need
        self.model=ptu.build_mlp(input_size=self.observation_dim,
                                 output_size=self.action_dim,
                                 n_layers=self.hyperparameters['n_layers'],
                                 size=self.hyperparameters['size'],
                                 )
        self.optimizer=optim.Adam(self.model.parameters(),
                                  lr=self.hyperparameters['lr'])
        self.loss=nn.MSELoss()


    def forward(self, observation: torch.FloatTensor):
        #*********YOUR CODE HERE******************
        action=self.model(observation) # change this to your action
        return action


    @torch.no_grad()
    def get_action(self, observation: torch.FloatTensor):
        if observation.dim() == 1:
            observation = observation.unsqueeze(0)
        action = self.model(observation)
        return action 

    
    def update(self, observations, actions):
        #*********YOUR CODE HERE******************
        pred_actions=self.model(observations)
        loss=self.loss(pred_actions,actions)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def train_iteration(self, env, envsteps_so_far, render=False, itr_num=None, **kwargs):
        '''
        Args:
            env: gym enviroment instance
            envsteps_so_for: how many steps the agent have used in environment while training
        Returns:
            dictionary with following keys:
                episode_loss: float value showing the the mean loss after updates (updates_per_iterations) 
                trajectories: a sampled trajectory at the end of the updates (refer function utils.sample_trajectories)
                current_train_envsteps: how many total steps of envionment taken in this iteation
        '''
        # Load expert
        if not hasattr(self, "expert_policy"):
            self.expert_policy = load_expert_policy(env, self.args.env_name)
            self.max_ret = -np.inf

            # to sample from replay buffer use:
            # self.replay_buffer.sample_batch(batch_size, required=<list of required keys>)

        # *** YOUR CODE HERE ******
        max_episode_length=self.hyperparameters['max_length']
        num_trajs=self.hyperparameters['num_trajs']
        batch_size=self.hyperparameters['batch_size']
        total_loss=[]
        num_updates=10 # ! asked on piazza

        # first we will get some data to train our neural network
        # here data will be trajectories/episodes
        # ! we might have to use policy blending here befroe sampling trajectories
        trajs,envstep_this_batch=sample_trajectories(env,self.expert_policy,num_trajs*max_episode_length,max_episode_length,render)
        self.replay_buffer.add_rollouts(trajs) # we will add these trajs into replay buffer to sample from them later
        for i in range(num_updates):
            s_a_pairs=self.replay_buffer.sample_batch(batch_size,required=['obs','acs'])
            loss=self.update(s_a_pairs['obs'],s_a_pairs['acs'])
            total_loss.append(loss)

        return {
            'episode_loss': float(np.mean(total_loss)),
            'trajectories': trajs,
            'current_train_envsteps': envstep_this_batch
        }
