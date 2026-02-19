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
        self.replay_buffer = ReplayBuffer(self.hyperparameters['buffer_size']) #you can set the max size of replay buffer if you want
        

        # initialize your model and optimizer and other variables you may need
        self.model=ptu.build_mlp(input_size=self.observation_dim,
                                 output_size=self.action_dim,
                                 n_layers=self.hyperparameters['n_layers'],
                                 size=self.hyperparameters['size'],
                                 )
        self.best_eval_return=-np.inf
        self.optimizer=optim.Adam(self.model.parameters(),lr=self.hyperparameters['lr'])
        self.loss=nn.MSELoss()


    def forward(self, observation: torch.FloatTensor):
        #*********YOUR CODE HERE******************
        action=self.model(observation) # change this to your action
        return action


    @torch.no_grad()
    def get_action(self, observation: torch.FloatTensor):
        if observation.dim()==1:
            observation=observation.unsqueeze(0)
        action=self.model(observation)
        return action 

    
    def update(self, observations, actions):
        #*********YOUR CODE HERE******************
        pred_actions=self.model(observations)
        loss=self.loss(pred_actions,actions)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()
    
    def blended_policy(self,beta):
        # this type of policy blending was used in dagger paper
        def policy(obs):
            if np.random.rand()<beta: # when beta is large this probability is high
                expert_ac=self.expert_policy.get_action(obs)
                if expert_ac.ndim==1:
                    expert_ac=expert_ac[np.newaxis,:] # add a batch dimension because learned policy was also giving unsqueezed output
                return ptu.from_numpy(expert_ac)
            else:
                return self.get_action(obs)
        return policy

    def relabel_with_expert(self, trajs):
        relabel_trajs=[]
        for traj in trajs:
            obs=traj['observation']
            obs_tensor=ptu.from_numpy(obs)
            expert_acs=self.expert_policy.get_action(obs_tensor)
            relabeled_traj={
                'observation': obs,
                'action': expert_acs,
                'reward': traj['reward'],
                'next_observation': traj['next_observation'],
                'terminal': traj['terminal'],
            }
            relabel_trajs.append(relabeled_traj)
            
        return relabel_trajs
    
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
        num_updates = self.hyperparameters['num_updates']
        save_freq = self.hyperparameters['save_freq']
        beta_p=self.hyperparameters['beta_p']
        total_loss=[]

        # first we will get some data to train our neural network
        # here data will be trajectories/rollouts 
        beta=beta_p**itr_num
        mixed_policy=self.blended_policy(beta)
        trajs,envstep_this_batch=sample_trajectories(env,mixed_policy,num_trajs*max_episode_length,max_episode_length,render)
        relabeled_trajs = self.relabel_with_expert(trajs)
        self.replay_buffer.add_rollouts(relabeled_trajs) # we will add these trajs into replay buffer to sample from them later
  
        for i in range(num_updates):
            s_a_pairs=self.replay_buffer.sample_batch(batch_size,required=['obs','acs']) # number of pairs (s,a)
            obs=ptu.from_numpy(s_a_pairs['obs'])
            acs=ptu.from_numpy(s_a_pairs['acs'])
            loss=self.update(obs,acs)
            total_loss.append(loss)

        if itr_num%save_freq==0:
            eval_trajs,_=sample_trajectories(env,self.get_action,10*max_episode_length,max_episode_length,render)
            eval_avg_return=np.mean([eval_traj['reward'].sum() for eval_traj in eval_trajs]) # we evaluate on the basis of average return of 10 trajectories
            if eval_avg_return>self.best_eval_return: # if it is better than the best return we have till now then we save the model
                self.best_eval_return=eval_avg_return
                save_path=os.path.join('best_models',f'{self.args.env_name}.pth')
                torch.save(self.model.state_dict(), save_path)
                print(f"Best model saved with Return: {eval_avg_return:.2f}")

        return {
            'episode_loss': float(np.mean(total_loss)),
            'trajectories': trajs,
            'current_train_envsteps': envstep_this_batch
        }
